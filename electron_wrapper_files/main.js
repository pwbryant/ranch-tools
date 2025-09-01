const { app, BrowserWindow } = require('electron');
const spawn = require('cross-spawn');
const path = require('path');
const http = require('http');
const fs = require('fs');

// Detect if running in development or production
const isDev = !app.isPackaged;


// Create log file path
const logPath = isDev
    ? path.join(__dirname, 'debug.log')
    : path.join(process.resourcesPath, '..', 'debug.log'); // Goes to install directory


function writeLog(message) {
    const timestamp = new Date().toISOString();
    const logEntry = `${timestamp}: ${message}\n`;
    fs.appendFileSync(logPath, logEntry);
}

let mainWindow;
let djangoProcess;

// Set paths based on environment
const DJANGO_PATH = isDev 
    ? path.join(__dirname, '..', 'django_project')
    : path.join(process.resourcesPath, 'django_project');

const PYTHON_PATH = isDev 
    ? path.join(__dirname, 'python-embed', 'python.exe')
    : path.join(process.resourcesPath, 'python-embed', 'python.exe');

console.log('Environment:', isDev ? 'Development' : 'Production');
console.log('Django Path:', DJANGO_PATH);
console.log('Python Path:', PYTHON_PATH);

function waitForDjango(callback, maxAttempts = 100) {
    let attempts = 0;
    
    const checkDjango = () => {
        attempts++;
        const req = http.get('http://localhost:8000/pregchecks', (res) => {
            writeLog('Django is ready!');
            console.log('Django is ready!');
            callback();
        });
        
        req.on('error', (err) => {
            if (attempts < maxAttempts) {
                console.log(`Waiting for Django... (attempt ${attempts})`);
                setTimeout(checkDjango, 1000);
            } else {
                console.error('Django failed to start within timeout period');
            }
        });
    };
    
    checkDjango();
}

function startDjango() {
    console.log('Starting Django server...');
    console.log('isDev:', isDev);
    console.log('Django Path exists:', require('fs').existsSync(DJANGO_PATH));
    console.log('Python Path exists:', require('fs').existsSync(PYTHON_PATH));

    writeLog('Starting Django server...');
    writeLog(`isDev: ${isDev}`);
    writeLog(`Django Path: ${DJANGO_PATH}`);
    writeLog(`Python Path: ${PYTHON_PATH}`);
    writeLog(`Django Path exists: ${fs.existsSync(DJANGO_PATH)}`);
    writeLog(`Python Path exists: ${fs.existsSync(PYTHON_PATH)}`);

    const SETTINGS_MODULE = 'config.settings.dev';
    
    // Fixed: Use djangoProcess (not debugProcess) and clean up the Python command
    djangoProcess = spawn(PYTHON_PATH, [
        '-c',
        `
import sys
import os

# Add Django project directory to Python path
current_dir = os.getcwd()
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Start Django server
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload', '--settings=${SETTINGS_MODULE}'])
        `
    ], {
        cwd: DJANGO_PATH,
        stdio: 'pipe'
    });
    
    djangoProcess.stdout.on('data', (data) => {
        console.log(`Django: ${data}`);
    });
    
    djangoProcess.stderr.on('data', (data) => {
        writeLog(`Django Error: ${data}`);
        console.log(`Django Error: ${data}`);
    });

    djangoProcess.on('error', (error) => {
        writeLog(`Failed to start Django: ${error}`);
        console.error('Failed to start Django:', error);
    });

    djangoProcess.on('exit', (code) => {
        console.log(`Django process exited with code ${code}`);
    });
}

function stopDjango() {
    if (djangoProcess) {
        console.log('Stopping Django server...');
        djangoProcess.kill();
        djangoProcess = null;
    }
}

function createWindow() {
    startDjango();

    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
        icon: path.join(__dirname, 'icon.png'),
    });

    // Wait for Django to be ready
    waitForDjango(() => {
        mainWindow.loadURL('http://localhost:8000/pregchecks');
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    stopDjango();
    app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

app.on('before-quit', () => {
    stopDjango();
});




// // Works except for stop
// const { app, BrowserWindow } = require('electron');
// const spawn = require('cross-spawn');
// const path = require('path');
// const http = require('http');

// let mainWindow;
// let djangoProcess;

// // Detect if running in development or production
// const isDev = !app.isPackaged;

// // Set paths based on environment
// const DJANGO_PATH = isDev 
//     ? path.join(__dirname, '..', 'django_project')
//     : path.join(process.resourcesPath, 'django_project');

// const PYTHON_PATH = isDev 
//     ? path.join(__dirname, 'python-embed', 'python.exe')
//     : path.join(process.resourcesPath, 'python-embed', 'python.exe');

// console.log('Environment:', isDev ? 'Development' : 'Production');
// console.log('Django Path:', DJANGO_PATH);
// console.log('Python Path:', PYTHON_PATH);

// function waitForDjango(callback, maxAttempts = 30) {
//     let attempts = 0;
    
//     const checkDjango = () => {
//         attempts++;
//         const req = http.get('http://localhost:8000/pregchecks', (res) => {
//             console.log('Django is ready!');
//             callback();
//         });
        
//         req.on('error', (err) => {
//             if (attempts < maxAttempts) {
//                 console.log(`Waiting for Django... (attempt ${attempts})`);
//                 setTimeout(checkDjango, 1000);
//             } else {
//                 console.error('Django failed to start within timeout period');
//             }
//         });
//     };
    
//     checkDjango();
// }


// function startDjango() {
//     console.log('Starting Django server...');
    
//     const SETTINGS_MODULE = 'config.settings.dev';
    
//     // Debug: Test what Python can actually import
//     const debugProcess = spawn(PYTHON_PATH, [
//         '-c',
//         `
// import sys
// import os

// # Add current directory to Python path
// current_dir = os.getcwd()
// if current_dir not in sys.path:
//     sys.path.insert(0, current_dir)

// print("Added to Python path:", current_dir)
// print("Testing config import...")

// try:
//     import config.settings.dev
//     print("SUCCESS: Can import config.settings.dev")
    
//     # Now start Django
//     from django.core.management import execute_from_command_line
//     execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload', '--settings=config.settings.dev'])
    
// except ImportError as e:
//     print("FAILED:", e)
//         `
//     ], {
//         cwd: DJANGO_PATH,
//         stdio: 'pipe'
//     });
    
//     debugProcess.stdout.on('data', (data) => {
//         console.log(`Debug: ${data}`);
//     });
    
//     debugProcess.stderr.on('data', (data) => {
//         console.log(`Debug Error: ${data}`);
//     });

// }

// function stopDjango() {
//     if (djangoProcess) {
//         console.log('Stopping Django server...');
//         djangoProcess.kill();
//         djangoProcess = null;
//     }
// }

// function createWindow() {
//     startDjango();

//     mainWindow = new BrowserWindow({
//         width: 1200,
//         height: 800,
//         webPreferences: {
//             nodeIntegration: true,
//             contextIsolation: false,
//         },
//         icon: path.join(__dirname, 'icon.png'),
//     });

//     // Wait for Django to be ready
//     waitForDjango(() => {
//         mainWindow.loadURL('http://localhost:8000/pregchecks');
//     });

//     mainWindow.on('closed', () => {
//         mainWindow = null;
//     });
// }

// app.whenReady().then(createWindow);

// app.on('window-all-closed', () => {
//     stopDjango();
//     app.quit();
// });

// app.on('activate', () => {
//     if (BrowserWindow.getAllWindows().length === 0) {
//         createWindow();
//     }
// });

// app.on('before-quit', () => {
//     stopDjango();
// });
