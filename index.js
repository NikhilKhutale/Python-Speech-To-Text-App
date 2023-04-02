import express from 'express';
import { spawn } from 'child_process';
import dotenv from "dotenv"
import path from "path"

dotenv.config();

const app = express();
const port = process.env.PORT || 5000;

console.log(path.resolve(__dirname, 'speech', 'dataGenerator.py'))

app.post('/api/start-recording', (req, res) => {
  // Execute the Python script as a child process
  const pythonProcess = spawn('python3', [path.resolve(__dirname, 'speech', 'sample1.py')]);


  let results = '';

  // Listen for data from the Python script
  pythonProcess.stdout.on('data', (data) => {
    results += data.toString();
  });

  // Listen for any errors from the Python script
  pythonProcess.stderr.on('data', (data) => {
    console.error(data.toString());
  });

  // When the Python script is done, send the results back to the client
  pythonProcess.on('close', (code) => {
    if (code === 0) {
      try {
        // Attempt to parse the Python script's output as JSON
        const parsedResults = JSON.parse(results);
        res.json(parsedResults);
      } catch (error) {
        // If the output cannot be parsed as JSON, return an error response
        res.status(500).send(`Unable to parse Python script output as JSON: ${error.message}`);
      }
    } else {
      res.status(500).send(`Python script exited with code ${code}`);
    }
  });
});

app.post('/api/generate-data', (req, res) => {
  // Execute the Python script as a child process
  const pythonProcess = spawn('python3', ['./speech/dataGenerator.py']);
  

  // Listen for any errors from the Python script
  pythonProcess.stderr.on('data', (data) => {
    console.error(data.toString());
    res.status(500).send(data.toString());
  });

  // When the Python script is done, send a success message back to the client
  pythonProcess.on('close', (code) => {
    if (code === 0) {
      res.send('Data generation complete!');
    } else {
      res.status(500).send(`Python script exited with code ${code}`);
    }
  });
});



if(process.env.NODE_ENV=='production'){

  app.get('/',(req,res)=>{
      app.use(express.static(path.resolve(__dirname,'client','build')))
      res.sendFile(path.resolve(__dirname,'client','build','index.html'))
  })
}


app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
