import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title as ChartTitle,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, ChartTitle, Tooltip, Legend);

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 70px;
  background-color: #000;
  min-height: 100vh;
  margin-bottom: 100px;
`;

const Title = styled.h1`
  color: #fff;
  font-weight: bold;
  margin-bottom: 20px;
`;

const ImageContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  background-color: #000;
  margin-bottom: 40px;
  width: 90%;
  border: 2px solid #fff;
  border-radius: 20px;
`;

const Container = styled.div`
  display: flex;
  justify-content: flex-start;
  align-items: center;
  overflow-x: auto;
  overflow-y: hidden;
  width: 100%;
  height: 170px; /* Adjust height based on viewport */
  background-color: #fff;

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

const StatsContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  width: 100%;
  max-width: 1200px;
  margin-bottom: 40px;
`;

const StatCard = styled.div`
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  flex: 1;
  margin: 10px;
`;

const StatValue = styled.h2`
  color: #2b8a3e;
  font-size: 2em;
  margin-bottom: 10px;
`;

const StatLabel = styled.p`
  color: #555;
`;

const ChartContainer = styled.div`
  width: 100%;
  max-width: 1200px;
`;

const ChartWrapper = styled.div`
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const ScrollableImage = () => {
  const [image, setImage] = useState(null);
  const [stats, setStats] = useState({ frequencies: {}, stability: {} });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5001/spectrogram/marked_spectrogram.png', {
          responseType: 'blob'
        });
        const imageObjectURL = URL.createObjectURL(response.data);
        setImage(imageObjectURL);
        fetchAnalyticsData();
      } catch (error) {
        console.error('Error fetching the image:', error);
        setImage(null); // Fallback to placeholder
      }
    };

    const fetchAnalyticsData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5001/api/analytics');
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching analytics data:', error);
      } finally {
        setLoading(false);
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

  if (loading) {
    return <Wrapper>Loading...</Wrapper>;
  }

  const renderFrequencies = () => {
    return Object.entries(stats.frequencies).map(([label, frequency]) => (
      <StatCard key={label}>
        <StatValue>{(frequency * 100).toFixed(2)}%</StatValue>
        <StatLabel>{label} Frequency</StatLabel>
      </StatCard>
    ));
  };

  // const renderStability = () => {
  //   return Object.entries(stats.stability).map(([label, stability]) => (
  //     <StatCard key={label}>
  //       <StatValue>{stability}</StatValue>
  //       <StatLabel>{label} Stability</StatLabel>
  //     </StatCard>
  //   ));
  // };

  const chartData = {
    labels: Object.keys(stats.frequencies),
    datasets: [
      {
        label: 'Frequency (%)',
        data: Object.values(stats.frequencies).map(frequency => frequency * 100),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Stability (consecutive labels)',
        data: Object.values(stats.stability),
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
      },
    ],
  };

  return (
    <Wrapper>
      <Title>Vocal Register Identification Analytics</Title>
      <ImageContainer>
        <Container>
          {image ? (
            <Image src={image} alt="Long Image" />
          ) : (
            <Placeholder>No Region Selected</Placeholder>
          )}
        </Container>
      </ImageContainer>
      <StatsContainer>
        {renderFrequencies()}
        {/* {renderStability()} */}
      </StatsContainer>
      <ChartContainer>
        <ChartWrapper>
          <h3 style={{ textAlign: 'center' }}>Frequency and Stability</h3>
          <Bar data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' }, title: { display: true, text: 'Frequency and Stability of Vocal Registers' } } }} />
        </ChartWrapper>
      </ChartContainer>
    </Wrapper>
  );
};

export default ScrollableImage;
