const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

async function transcribeAudio() {
    const inputFile = '/Users/bozhang/Desktop/Mifo Manager.m4a';
    const outputDir = '/Users/bozhang/Desktop';
    const outputFile = path.join(outputDir, 'test transcribe.txt');
    
    console.log('Starting transcription...');
    console.log(`Input: ${inputFile}`);
    console.log(`Output: ${outputFile}`);
    
    // Run whisper
    const whisperProcess = spawn('whisper', [
        inputFile,
        '--model', 'base',
        '--output_format', 'txt',
        '--output_dir', outputDir
    ]);
    
    whisperProcess.stdout.on('data', (data) => {
        console.log(`Whisper: ${data}`);
    });
    
    whisperProcess.stderr.on('data', (data) => {
        console.log(`Progress: ${data}`);
    });
    
    whisperProcess.on('close', async (code) => {
        if (code === 0) {
            console.log('\nTranscription completed successfully!');
            
            // Find the generated file and rename it
            try {
                const files = await fs.readdir(outputDir);
                const generatedFile = files.find(f => 
                    f.startsWith('Mifo Manager') && f.endsWith('.txt')
                );
                
                if (generatedFile) {
                    const oldPath = path.join(outputDir, generatedFile);
                    await fs.rename(oldPath, outputFile);
                    console.log(`\nTranscription saved to: ${outputFile}`);
                    
                    // Read and display a preview
                    const content = await fs.readFile(outputFile, 'utf-8');
                    console.log('\n--- Preview (first 500 chars) ---');
                    console.log(content.substring(0, 500) + '...');
                }
            } catch (error) {
                console.error('Error renaming file:', error);
            }
        } else {
            console.error(`Whisper process exited with code ${code}`);
        }
    });
    
    whisperProcess.on('error', (error) => {
        console.error('Error running whisper:', error);
        console.log('\nMake sure Whisper is installed:');
        console.log('pip3 install openai-whisper');
    });
}

transcribeAudio();