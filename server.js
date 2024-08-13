const express = require('express');
const mongoose = require('mongoose');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const { PythonShell } = require('python-shell');

const app = express();
const PORT = process.env.PORT || 3000;

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/audioFiles', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

// Define a schema and model for storing audio files
const audioSchema = new mongoose.Schema({
    filename: String,
    contentType: String,
    audio: Buffer,
});

const Audio = mongoose.model('Audio', audioSchema);

// Set up multer for file uploads
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Endpoint to upload audio
app.post('/upload', upload.single('audio'), async (req, res) => {
    const audioFile = new Audio({
        filename: req.file.originalname,
        contentType: req.file.mimetype,
        audio: req.file.buffer,
    });

    await audioFile.save();

    res.status(200).json({ message: 'Audio file uploaded successfully!', audioId: audioFile._id });
});

// Function to detect keywords and generate TTS response
function generateTTSResponse(transcription) {
    let response = '';
    if (transcription.includes('place order')) {
        response = 'Placing your order.';
    } else if (transcription.includes('add to cart')) {
        response = 'Adding the item to your cart.';
    } else if (transcription.includes('voice authentication')) {
        response = 'Voice authentication required for wallet access.';
    } else {
        response = `You said: ${transcription}`;
    }
    return response;
}

// Endpoint to fetch, transcribe, and provide TTS feedback
app.get('/transcribe/:id', async (req, res) => {
    try {
        const audio = await Audio.findById(req.params.id);

        if (!audio) {
            return res.status(404).json({ message: 'Audio not found' });
        }

        // Save the audio buffer to a temporary file
        const tempFilePath = path.join(__dirname, 'recorded_audio.wav');
        fs.writeFileSync(tempFilePath, audio.audio);

        // Run Whisper model on the saved file
        exec(`python transcribe.py`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing Whisper: ${error.message}`);
                return res.status(500).json({ message: 'Error transcribing audio' });
            }

            const transcription = stdout.trim();
            const ttsResponse = generateTTSResponse(transcription);

            // Save the TTS response as an audio file (using a Python script)
            PythonShell.run('generate_tts.py', { args: [ttsResponse] }, function (err) {
                if (err) throw err;
                console.log('TTS audio generated');
                
                // Send the TTS response back to the frontend
                res.json({ transcription: transcription, ttsResponse: ttsResponse, ttsAudio: '/tts_output.wav' });
            });

            // Clean up the temporary file
            fs.unlinkSync(tempFilePath);
        });
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

// Serve the frontend
app.use(express.static(path.join(__dirname, 'public')));

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
