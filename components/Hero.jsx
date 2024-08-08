import React from 'react';
import {Link} from "react-router-dom";


const Hero = () => {
  return (
    <div className = 'text-white'>
        <div className = 'max-w-[800px] mt-[-96px] w-full h-screen mx-auto text-center flex flex-col justify-center'>
            <p className = 'text-[#00df9a] font-bold p-2'>SING WITH MACHINE LEARNING</p>
            <h1 className = 'md:text-7xl sm:text-6xl text-4xl font-bold md:py-6'>Automatic Vocal Register Analysis</h1>
            
            <p className = 'md:text-5xl sm:text-4xl text-xl fond-bold'>Powered by SVM, CNN</p>
            <div className = 'flex flex-row w-full justify-center'>
              <Link to="/demo">
                  <button className = 'bg-[#00df9a] w-[200px] rounded-md font-medium my-6 ml-auto mr-5 py-3 text-black'>
                      Try It Out!
                  </button>
              </Link>
              <Link to = 'https://github.com/akim42003/AVRA.git'>
                  <button className = 'bg-[#00df9a] w-[200px] rounded-md font-medium my-6 mx-auto py-3 text-black'>
                      Read More
                  </button>
              </Link>
            </div>
        </div>
    </div>
  )
}

export default Hero
