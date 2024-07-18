import React from 'react';
import Navbar from './Navbar';
import Footer from './Footer';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  margin-top: 0px;
  height: 1000px;
  background-color: #56595C;
`;

const CardContainer = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 200px;
  margin-top: 0px;
  background-color: #56595C;
`;

const Card = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 50px;
  width: 250px;
  margin: 30px;
  background-color: #000;
  border-radius: 25px;
`;

const ArrowContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 50px;
`;

const Arrow = styled.div`
  width: 0;
  height: 0;
  border-top: 15px solid transparent;
  border-bottom: 15px solid transparent;
  border-left: 15px solid white; /* Adjust color as needed */
`;

const ArrowComponent = () => (
  <ArrowContainer>
    <Arrow />
  </ArrowContainer>
);

const About = () => {
  return (
    <div>
      <Navbar/>
      <Container>
        <h1 className='text-white font-bold text-5xl mt-20 mb-10'>Meet AVRA</h1>
        <div className='flex max-w-[85%]'>
          <p className='text-white font-semibold text-2xl'>
            AVRA (Automatic Vocal Register Analysis) is a machine learning tool that classifies isolated vocal audio clips
            into four vocal registers: Chest Voice, Mix, Head-Mix, Head Voice. Options for an SVM and Convolutional Neural Network are given with SVM as the default model. 
            The audio-spectrogram processing pipeline is described as follows:
          </p>
        </div>
      <CardContainer>
        <Card>
          <div className='flex text-center mx-5 mt-[5px]'>
            <p className='text-white text-sm font-semibold'>Audio Splitting and Spectrogram Synthesis</p>
          </div>
        </Card>
        <ArrowComponent />
        <Card>
          <div className='flex text-center mt-[5px] mx-5'>
            <p className='text-white text-sm font-semibold'>Spectrogram Processing and Model Evaluation</p>
          </div>
        </Card>
        <ArrowComponent />
        <Card>
          <div className='flex text-center mt-[5px] mx-5'>
            <p className='text-white text-sm font-semibold'>Label Processing and Image Output</p>
          </div>
        </Card>
      </CardContainer>
        <div className = 'flex flex-col w-[85%]'>
            <h1 className = 'text-white font-bold text-3xl mb-8'>1. Audio Processing</h1>
            <p className = 'text-white font-semibold text-lg ml-14'> The user selects a pre-separated vocal track (via Demucs, Logic, etc) which is then split into three second files. 
                Each file is then rendered into a 154x1024 mel-spectrogram which is split into 154x128 images. Spectrograms are rendered using Librosa and with the default mel-scale parameters from Audacity.
            </p>
            <h1 className = 'text-white font-bold text-3xl mt-8 mb-8'>2. Pre-processing and Model Architecture</h1>
            <h1 className = 'text-white font-bold text-3xl mt-8 mb-8'>3. Post-processing</h1>
        </div>
      </Container>
      <Footer/>
    </div>
  );
}

export default About;
