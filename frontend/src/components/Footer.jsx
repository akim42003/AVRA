import React from 'react'
import {FaGithubSquare, FaInstagram, FaTwitterSquare} from 'react-icons/fa'

const Footer = () => {
  return (
    <div className = 'max-w-[1240px] mx-auto py-16 px-4 grid lg:grid-cols-2 gap-8 text-gray-300'>
        <h1 className = 'w-full text-3xl font-bold text-[#00df9a]'>AVRA.</h1>
        <div className = 'lg:col-span-2 flex justify-between'>
                <p className = 'flex justify-between font-bold text-xl'>Home</p>
                <p className = 'flex justify-between font-bold text-xl'>About</p>
                <p className = 'flex justify-between font-bold text-xl'>Demo</p>
        </div>
        <div>
            <div className = 'flex justify-between '>
                <FaGithubSquare size = {30}/>
                <FaInstagram size = {30}/>
                <FaTwitterSquare size = {30}/>
            </div>
        </div>
    </div>
  )
}

export default Footer