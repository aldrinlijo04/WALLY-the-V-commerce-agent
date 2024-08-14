const express = require('express');
const mongoose = require('mongoose');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

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

    // Save the file to the recordings folder
    const filePath = path.join(__dirname, 'recordings', req.file.originalname);
    fs.writeFileSync(filePath, req.file.buffer);

    // Execute the Python script for transcription
    exec('python transcribe.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return res.status(500).json({ message: 'Error during transcription' });
        }
        if (stderr) {
            console.error(`Python script stderr: ${stderr}`);
            return res.status(500).json({ message: 'Error during transcription' });
        }
        console.log(`Python script output: ${stdout}`);
        res.status(200).json({ message: 'Audio file uploaded and transcribed successfully!', transcription: stdout });
    });
});

// Serve the frontend
app.use(express.static(path.join(__dirname, 'public')));

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
