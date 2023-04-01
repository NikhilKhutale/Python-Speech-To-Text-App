
import './App.css';

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Swal from 'sweetalert2';
import { CircularProgress } from '@mui/material';

function App() {
  const [transcription, setTranscription] = useState({ "text": "", "queried_data": [] });
  const [loading, setLoading] = useState(false)
  const [dataLoading, setDataLoading] = useState(false)

  useEffect(() => {
    if (transcription.text.length > 0) {
      const message = new SpeechSynthesisUtterance(`There are total ${transcription.queried_data.length} points with low range.`);
      window.speechSynthesis.speak(message);
    }
  }, [transcription]);


  const handleStartRecording = async () => {
    try {
      setTimeout(() => setLoading(true), 2000);
      const response = await axios.post('api/start-recording');
      console.log(response);
      setTranscription(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false)
    }
  };

  const handleGeneratData = async () => {
    try {
      setDataLoading(true)
      const response = await axios.post('api/generate-data');
      console.log(response);
      Swal.fire({
        title: response.data,
        icon: "success",
        button: "OK",
      });
    } catch (error) {
      console.error(error);
    } finally {
      setDataLoading(false)
    }
  }


  return (
    <div className='App'>
      <div className='generate-data'>
        <button className='generate-data-btn' onClick={handleGeneratData}>{dataLoading ? <CircularProgress sx={{ color: "#a8bffc" }} size={20} /> : "Generate-data"}</button>
      </div>
      <div className='microphone-div'>
        <p>Try saying state or district name</p>
        <button className='microphone-btn' onClick={handleStartRecording}><i className={`fa-solid fa-microphone fa-2xl ${loading && 'fa-beat'}`}></i></button>

      </div>
      {transcription.text.length > 0 && (
        <>
          <p>{transcription.text}</p>
          <p>There are total {transcription.queried_data.length} points with low range.</p>
          {transcription.queried_data.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Latitude</th>
                  <th>Longitude</th>
                  <th>District</th>
                  <th>State</th>
                  <th>Pincode</th>
                  <th>Temperature</th>
                  <th>Humidity</th>
                  <th>Air Quality</th>
                  <th>Range</th>
                </tr>
              </thead>
              <tbody>
                {transcription.queried_data.map((row) => (
                  <tr key={row.id}>
                    <td>{row.id}</td>
                    <td>{row.latitude}</td>
                    <td>{row.longitude}</td>
                    <td>{row.district}</td>
                    <td>{row.state}</td>
                    <td>{row.pincode}</td>
                    <td>{row.temperature}</td>
                    <td>{row.humidity}</td>
                    <td>{row.air_Quality}</td>
                    <td>{row.range}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>There is no data for low range</p>
          )}
        </>
      )}
    </div>
  );
}

export default App;


