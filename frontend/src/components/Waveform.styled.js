import styled from 'styled-components';

export const WaveformContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 270px;
  width: 100%;
  background-color: #000;
`;

export const ButtonContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top; 20px;
  margin-bottom: 20px; /* Space between buttons and waveform */
  height: 90px; /* Fixed the typo here */
  width: 100%;
  background-color: #000;
`;

export const Wave = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* Fixed the value here */
  width: 90%;
  height: 120px;
  background-color: #000;
  border: 2px solid #fff;
`;

export const PlayButton = styled.button`
  width: 100px; /* Set the width to make it rectangular */
  height: 50px; /* Set the height to make it rectangular */
  margin: 10px; /* Add margin to ensure buttons do not overlap */
  padding: 10px 20px;
  background-color: #2D5BFF;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 20px; /* Ensure there is no border-radius for sharp corners */
  display: flex;
  align-items: center;
  justify-content: center; /* Center the text within the button */

  &:hover {
    background-color: #1A3FB7;
  }
`;

export const HiddenFileInput = styled.input`
  display: none;
`;

export const CustomFileInputButton = styled.button`
  width: 100px; /* Set the width to make it rectangular */
  height: 50px; /* Set the height to make it rectangular */
  margin: 10px; /* Add margin to ensure buttons do not overlap */
  padding: 10px 20px;
  background-color: #2D5BFF;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 20px; /* Ensure there is no border-radius for sharp corners */
  display: flex;
  align-items: center;
  justify-content: center; /* Center the text within the button */

  &:hover {
    background-color: #1A3FB7;
  }
`;

export const Slider = styled.input.attrs({ type: 'range' })`
  -webkit-appearance: none;
  width: 300px;
  height: 10px;
  margin: 20px;
  background: #EFEFEF;
  border-radius: 5px;
  outline: none;
  padding: 0;
  cursor: pointer;
  transition: background 0.3s;

  &:hover {
    background: #1A3FB7;
  }

  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    background: #2D5BFF;
    border-radius: 50%;
    cursor: pointer;
    transition: background 0.3s;
  }

  &::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: #2D5BFF;
    border-radius: 50%;
    cursor: pointer;
    transition: background 0.3s;
  }

  &:hover::-webkit-slider-thumb {
    background: #1A3FB7;
  }

  &:hover::-moz-range-thumb {
    background: #1A3FB7;
  }

  &:focus::-webkit-slider-thumb {
    box-shadow: 0 0 5px #1A3FB7;
  }

  &:focus::-moz-range-thumb {
    box-shadow: 0 0 5px #1A3FB7;
  }

  &:active::-webkit-slider-thumb {
    background: #0D1E6D;
  }

  &:active::-moz-range-thumb {
    background: #0D1E6D;
  }
`;

export const TimelineContainer = styled.div`
  width: 100%;
  height: 40px;
  background-color: #fff;
`;

export const Image = styled.img`
  height: 154px;
  width: 90%;
`