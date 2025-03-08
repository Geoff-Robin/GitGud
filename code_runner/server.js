const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const { tmpdir } = require('os');

const app = express();
app.use(bodyParser.json());

app.post('/execute', (req, res) => {
    const { language, code } = req.body;

    const tempDir = './temp';
    if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir);
    }

    let command;
    switch (language) {
        case 'python':
            const filename_py = path.join(tempDir,'temp.py')
            fs.writeFileSync(filename_py,code);
            command = `python3 -c temp/${filename_py}`;
            break;
        case 'c':
            const filename_c = path.join(tempDir,'temp.c');
            const executable_c = path.join(tempDir,'temp_executable')
            fs.writeFileSync(filename_c, code);
            command = `g++ temp/${filename_c} -o ${executable_c} ; ${executable_c}`;
            break;
        case 'c++': 
            const filename_cpp = path.join(tempDir, 'temp.cpp');
            const executable_cpp = path.join(tempDir, 'temp_executable');
            fs.writeFileSync(filename_cpp, code);
            command = `g++ ${filename_cpp} -o ${executable_cpp} ; ${executable_cpp}`;
            break;
        default:
            return res.status(400).send('Unsupported language');
    }

    exec(command, (error, stdout, stderr) => {
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
