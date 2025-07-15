const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const fsPromises = require('fs').promises;
const { spawn } = require('child_process');
const { v4: uuidv4 } = require('uuid');
const PDFDocument = require('pdfkit');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../uploads');
    await fsPromises.mkdir(uploadDir, { recursive: true });
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueId = uuidv4();
    const ext = path.extname(file.originalname);
    cb(null, `${uniqueId}${ext}`);
  }
});

const upload = multer({
  storage,
  limits: { fileSize: 100 * 1024 * 1024 }, // 100MB
  fileFilter: (req, file, cb) => {
    const allowedTypes = /mp3|wav|m4a|flac|ogg|webm|mp4|mpeg|mpga|oga|opus/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (extname || mimetype) {
      return cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only audio files are allowed.'));
    }
  }
});

const transcriptions = new Map();

app.post('/api/upload', upload.single('audio'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const { model = 'base', language = 'auto' } = req.body;
    const transcriptionId = uuidv4();
    
    transcriptions.set(transcriptionId, {
      id: transcriptionId,
      filename: req.file.originalname,
      status: 'processing',
      progress: 0,
      model,
      language,
      startTime: Date.now()
    });

    processTranscription(transcriptionId, req.file.path, model, language);

    res.json({ 
      transcriptionId,
      message: 'File uploaded successfully, transcription started' 
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/status/:id', (req, res) => {
  const transcription = transcriptions.get(req.params.id);
  
  if (!transcription) {
    return res.status(404).json({ error: 'Transcription not found' });
  }

  res.json(transcription);
});

app.get('/api/download/:id/:format', async (req, res) => {
  const { id, format } = req.params;
  const transcription = transcriptions.get(id);

  if (!transcription || transcription.status !== 'completed') {
    return res.status(404).json({ error: 'Transcription not found or not completed' });
  }

  const transcriptionDir = path.join(__dirname, '../transcriptions');
  
  if (format === 'txt') {
    const txtPath = path.join(transcriptionDir, `${id}.txt`);
    res.download(txtPath, `transcription_${transcription.filename}.txt`);
  } else if (format === 'pdf') {
    const pdfPath = path.join(transcriptionDir, `${id}.pdf`);
    res.download(pdfPath, `transcription_${transcription.filename}.pdf`);
  } else {
    res.status(400).json({ error: 'Invalid format' });
  }
});

async function processTranscription(id, audioPath, model, language) {
  const transcription = transcriptions.get(id);
  const transcriptionDir = path.join(__dirname, '../transcriptions');
  await fsPromises.mkdir(transcriptionDir, { recursive: true });

  try {
    const outputPath = path.join(transcriptionDir, `${id}.txt`);
    
    const args = [audioPath, '--model', model, '--output_format', 'txt', '--output_dir', transcriptionDir];
    
    if (language !== 'auto') {
      args.push('--language', language);
    }

    const whisperProcess = spawn('whisper', args);
    
    let stderr = '';
    
    whisperProcess.stderr.on('data', (data) => {
      stderr += data.toString();
      console.log('Whisper stderr:', data.toString());
      
      // Whisper doesn't output percentage progress, so we'll simulate it
      // based on detected language and processing stages
      if (stderr.includes('Detecting language')) {
        transcription.progress = 10;
        transcriptions.set(id, transcription);
      } else if (stderr.includes('Detected language')) {
        transcription.progress = 20;
        transcriptions.set(id, transcription);
      } else if (transcription.progress < 90) {
        // Gradually increase progress during processing
        transcription.progress = Math.min(90, transcription.progress + 5);
        transcriptions.set(id, transcription);
      }
    });
    
    whisperProcess.stdout.on('data', (data) => {
      console.log('Whisper stdout:', data.toString());
      // Update progress as we receive output
      if (transcription.progress < 80) {
        transcription.progress = Math.min(80, transcription.progress + 10);
        transcriptions.set(id, transcription);
      }
    });

    whisperProcess.on('close', async (code) => {
      if (code === 0) {
        try {
          const files = await fsPromises.readdir(transcriptionDir);
          const txtFile = files.find(f => f.startsWith(path.basename(audioPath, path.extname(audioPath))) && f.endsWith('.txt'));
          
          if (txtFile) {
            const oldPath = path.join(transcriptionDir, txtFile);
            const newPath = path.join(transcriptionDir, `${id}.txt`);
            await fsPromises.rename(oldPath, newPath);
            
            const text = await fsPromises.readFile(newPath, 'utf-8');
            
            await generatePDF(id, text, transcription.filename);
            
            transcription.status = 'completed';
            transcription.progress = 100;
            transcription.text = text;
            transcription.endTime = Date.now();
          } else {
            throw new Error('Transcription file not found');
          }
        } catch (error) {
          transcription.status = 'error';
          transcription.error = error.message;
        }
      } else {
        transcription.status = 'error';
        transcription.error = `Whisper process exited with code ${code}: ${stderr}`;
      }
      
      transcriptions.set(id, transcription);
      
      setTimeout(async () => {
        try {
          await fsPromises.unlink(audioPath);
        } catch (error) {
          console.error('Error cleaning up audio file:', error);
        }
      }, 5000);
    });

    whisperProcess.on('error', (error) => {
      transcription.status = 'error';
      transcription.error = error.message;
      transcriptions.set(id, transcription);
    });

  } catch (error) {
    transcription.status = 'error';
    transcription.error = error.message;
    transcriptions.set(id, transcription);
  }
}

async function generatePDF(id, text, originalFilename) {
  const pdfPath = path.join(__dirname, '../transcriptions', `${id}.pdf`);
  const doc = new PDFDocument();
  const stream = doc.pipe(fs.createWriteStream(pdfPath));

  doc.fontSize(20).text('Audio Transcription', { align: 'center' });
  doc.moveDown();
  doc.fontSize(12).text(`Original File: ${originalFilename}`, { align: 'left' });
  doc.text(`Date: ${new Date().toLocaleString()}`, { align: 'left' });
  doc.moveDown();
  doc.fontSize(11).text(text, { align: 'justify' });

  doc.end();
  await new Promise(resolve => stream.on('finish', resolve));
}

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

module.exports = app;