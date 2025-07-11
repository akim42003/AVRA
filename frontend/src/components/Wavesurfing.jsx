import React, { useRef, useEffect, useState } from 'react';
import WaveSurfer from 'wavesurfer.js';
import RegionsPlugin from 'wavesurfer.js/dist/plugins/regions.esm.js';
import TimelinePlugin from 'wavesurfer.js/dist/plugins/timeline.esm.js';
import axios from 'axios';
import { WaveformContainer, ButtonContainer, Wave, PlayButton, HiddenFileInput, CustomFileInputButton, Slider, TimelineContainer } from './Waveform.styled';

const Waveform = () => {
  const [loading, setLoading] = useState(false);
  const [useSVM, setUseSVM] = useState(false);
  const [useCNN, setUseCNN] = useState(false);
  const fileInputRef = useRef(null);
  const sliderRef = useRef(null);
  const waveformRef = useRef(null);
  const regionsPluginRef = useRef(null);
  const startRef = useRef(null);

  useEffect(() => {
    if (!waveformRef.current) {
      waveformRef.current = WaveSurfer.create({
        container: '#waveform',
        cursorWidth: 1,
        backend: 'MediaElement',
        height: 100,
        progressColor: '#00df9a',
        responsive: true,
        autoCenter: true,
        fillParent: true,
        normalize: true,
        splitChannels: false,
        interact: true,
        autoScroll: true,
        waveColor: '#EFEFEF',
        cursorColor: '#ddd5e9',
        mediaControls: true,
        minPxPerSec: 100,
        dragToSeek: true,
        plugins: [
          TimelinePlugin.create({
            container: '#timeline'
          })
        ]
      });

      regionsPluginRef.current = waveformRef.current.registerPlugin(RegionsPlugin.create());

      waveformRef.current.once('decode', () => {
        const slider = sliderRef.current;
        slider.addEventListener('input', (e) => {
          const minPxPerSec = e.target.valueAsNumber;
          waveformRef.current.zoom(minPxPerSec);
        });
      });

      return () => {
        if (waveformRef.current) {
          waveformRef.current.destroy();
          waveformRef.current = null;
        }
      };
    }
  }, []);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', file);

      try {
        await axios.post('http://127.0.0.1:5001/upload-file', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        
        const reader = new FileReader();
        reader.onload = (e) => {
          waveformRef.current.load(e.target.result);
          setLoading(false);
        };
        reader.readAsDataURL(file);
      } catch (error) {
        console.error('File upload error:', error);
        setLoading(false);
      }
    }
  };

  const createRegion = () => {
    if (regionsPluginRef.current) {
      regionsPluginRef.current.enableDragSelection({
        color: 'rgba(255, 0, 0, 0.25)',
      });
      const start = waveformRef.current.getCurrentTime();
      startRef.current = start;
    }
  };

  const handleRegionSave = () => {
    const end = waveformRef.current.getCurrentTime();
    const start = startRef.current;
    const stop = 0;

    axios.post('http://127.0.0.1:5001/save-region', {
      start,
      end,
      stop,
      useSVM,
      useCNN
    })
      .then(response => {
        console.log('Region saved successfully');
        // Dispatch the custom event to trigger image refresh
        const event = new CustomEvent('refreshImage');
        window.dispatchEvent(event);
      })
      .catch(error => {
        console.error('Error saving region:', error);
      });
  };

  const handleStop = () => {
    waveformRef.current.stop();
    waveformRef.current.seekTo(0);

    if (regionsPluginRef.current) {
      regionsPluginRef.current.destroy();
      regionsPluginRef.current = waveformRef.current.registerPlugin(RegionsPlugin.create());
      axios.post('http://127.0.0.1:5001/save-region', {
        start: 0,
        end: 0,
        stop: 1,
        useSVM: false,
        useCNN: false
      })
        .then(response => {
          console.log('Region reset successfully');
          // Dispatch the custom event to trigger image refresh
          const event = new CustomEvent('refreshImage');
          window.dispatchEvent(event);
        })
        .catch(error => {
          console.error('Error resetting region:', error);
        });
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <WaveformContainer>
      <ButtonContainer>
        <p className='text-white'>Zoom:</p>
        <Slider
          type="range"
          min="0.1"
          max="100"
          defaultValue="0.1"
          ref={sliderRef}
        />
        <CustomFileInputButton onClick={triggerFileInput}>
          Choose File
        </CustomFileInputButton>
        <HiddenFileInput
          type="file"
          accept="audio/*"
          ref={fileInputRef}
          onChange={handleFileChange}
        />
        <PlayButton onClick={handleRegionSave}>
          Save Region
        </PlayButton>
        <PlayButton onClick={handleStop}>
          Reset
        </PlayButton>
        <PlayButton onClick={createRegion}>
          Create Region
        </PlayButton>
        <div>
          <label className="text-white mr-3 ml-1">
            <input
              type="checkbox"
              checked={useSVM}
              onChange={() => setUseSVM(!useSVM)}
            />
            Use SVM
          </label>
        </div>
        <div>
          <label className="text-white">
            <input
              type="checkbox"
              checked={useCNN}
              onChange={() => setUseCNN(!useCNN)}
            />
            Use CNN
          </label>
        </div>
      </ButtonContainer>
      <p className="text-white flex justify-center font-bold">Selected Audio File</p>
      <Wave id='waveform'>
        {loading && <div className='text-white flex justify-center'>Loading...</div>}
        <TimelineContainer id='timeline' />
      </Wave>
    </WaveformContainer>
  );
};

export default Waveform;
