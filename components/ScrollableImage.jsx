import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  margin-top: 70px;
  background-color: #000;
`;

const Container = styled.div`
  display: flex;
  justify-content: flex-start;
  align-items: center;
  overflow-x: auto;
  overflow-y: hidden;
  width: 90%;
  height: 166px; /* Adjust height based on viewport */
  background-color: #fff;
  border: 2px solid #fff;

  &::-webkit-scrollbar {
    height: 12px;
  }
  &::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 10px;
  }
  &::-webkit-scrollbar-thumb:hover {
    background: #555;
  }
`;

const Image = styled.img`
  max-height: 100%; /* Scale image to fit container height */
  width: auto; /* Maintain aspect ratio */
  max-width: none;
`;

const Placeholder = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  font-size: 16px;
  color: #888;
`;

const ScrollableImage = () => {
  const [image, setImage] = useState(null);

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5001/spectrogram/marked_spectrogram.png', {
          responseType: 'blob'
        });
        const imageObjectURL = URL.createObjectURL(response.data);
        setImage(imageObjectURL);
      } catch (error) {
        console.error('Error fetching the image:', error);
        setImage(null); // Fallback to placeholder
      }
    };

    const handleRefresh = () => {
      fetchImage();
    };

    window.addEventListener('refreshImage', handleRefresh);

    // Initial fetch
    fetchImage();

    return () => {
      window.removeEventListener('refreshImage', handleRefresh);
    };
  }, []);

  return (
    <Wrapper>
      <p className="text-white flex justify-center font-bold">Spectrogram of Selected Region</p>
      <Container>
        {image ? (
          <Image src={image} alt="Long Image" />
        ) : (
          <Placeholder>No Region Selected</Placeholder>
        )}
      </Container>
    </Wrapper>
  );
};

export default ScrollableImage;
