const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(bodyParser.json());

const tempDir = path.join(__dirname, 'temp');
if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir);
}

app.post('/execute', (req, res) => {
    const { language, code } = req.body;
    let command;
    let filename, executable;

    switch (language) {
        case 'python':
            filename = path.join(tempDir, 'temp.py');
            fs.writeFileSync(filename, code);
            command = `python3 ${filename}`;
            break;
        case 'c':
        case 'c++':
            const extension = language === 'c' ? 'c' : 'cpp';
            filename = path.join(tempDir, `temp.${extension}`);
            executable = path.join(tempDir, 'temp_executable');
            fs.writeFileSync(filename, code);
            command = `g++ ${filename} -o ${executable} && ${executable}`;
            break;
        default:
            return res.status(400).send('Unsupported language');
    }

    exec(command, (error, stdout, stderr) => {
        fs.unlinkSync(filename);
        if (executable && fs.existsSync(executable)) fs.unlinkSync(executable);

        if (error) {
            return res.status(500).send(stderr);
        }
        res.send(stdout);
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
