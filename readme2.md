<task>
'projects/photobooth/src/' (see below for folder content) , give suggestion about improve project
</task>

<folder_content path="projects/photobooth/src/">
├── App.css
├── App.jsx
├── assets/
├── Camera.jsx
├── Error.jsx
├── index.css
├── lib/
├── LoadingPage.jsx
├── main.jsx
├── Result.jsx
├── SceneSlider.jsx
├── supabaseClient.js
├── Swap.jsx
└── theme-slider.jsx

<file_content path="projects/photobooth/src/App.css">

</file_content>

<file_content path="projects/photobooth/src/App.jsx">
import { useState } from 'react'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import './App.css'
import Camer from './Camera'
import Error from './Error'
import LoadingPage from './LoadingPage'
import Result from './Result'
import Swap from './Swap'
function App() {
  const [count, setCount] = useState(0)
  const backgroundImage = "https://fuhqxfbyvrklxggecynt.supabase.co/storage/v1/object/public/nielsen/backgrounds/bgggg.jpg";
  const camera= "/camera.png";
  return (
    <Router>
    <div
      className="text-center w-screen h-screen"
      style={{ backgroundImage: `url(${backgroundImage})`, backgroundSize: 'cover', backgroundPosition: 'center' }}
    >
      <Routes>
        <Route path="/" element={<Camer />} />
        {/* <Route path="/1" element={<ThemeSlider />} /> */}
        <Route path="/swap" element={<Swap />} />
        <Route path="/result" element={<Result />} />
        <Route path="/loading" element={<LoadingPage />} />
        <Route path="/error" element={<Error />} />

      </Routes>
    </div>
  </Router>
  )
}

export default App

</file_content>

<file_content path="projects/photobooth/src/Camera.jsx">
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import SceneSlider from "./SceneSlider";
import { ThemeSlider } from "./theme-slider";
import female from "/assets/female.png";
import male from "/assets/male.png";
import Futuristic from "/Futuristic.png";
import outerspace from "/outerspace.png";
import redcarpet from "/redcarpet.png";

const imgStyle = {
  width: "auto",
  height: "auto",
  maxWidth: "400px",
  maxHeight: "250px",
  objectFit: "contain",
  justifyContent: "center",
  alignItems: "center",
  cursor: "pointer",
  border: "5px solid #FFCE00",
};

const StyledInput = styled.input`
  padding-left: 35px;
  font-size: 34px;
  border: none;
  text-align: left;
  color: #182060;
  font-weight: bold;
  width: 760px;
  height: 110px;
  text-transform: capitalize;
  background-color: #fff;
  border-radius: 10px;
  &::placeholder {
    color: #182060;
  }
  margin-bottom: 20px;
`;

const StyledSelect = styled.select`
  padding-left: 35px;
  font-size: 34px;
  border: none;
  text-align: left;
  color: #182060;
  font-weight: bold;
  width: 830px;
  height: 110px;
  text-transform: capitalize;
  background-color: #fff;
  appearance: none;
  border-radius: 10px;
  &::placeholder {
    color: #182060;
  }
`;

const StyledButton = styled.button`
  background-color: #fff;
  color: #182060;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 30px;
`;

const SubmitButton = styled.button`
  background-image: url('https://fuhqxfbyvrklxggecynt.supabase.co/storage/v1/object/public/nielsen/button-backgrounds/1741586572972-submit.png');
  background-repeat: no-repeat;
  background-size: 100% 100%;
  background-color: transparent;
  border: none;
  cursor: pointer;
  text-indent: -9999px;
  position: relative;
  margin-top: 90px;
  background-size: cover;
  color: #fff;
  font-size: 34px;
  font-weight: bold;
  text-indent: 0;
  line-height: 104px;
`;

const backgroundImage = 'https://fuhqxfbyvrklxggecynt.supabase.co/storage/v1/object/public/nielsen/backgrounds/1741599792665-bggg.jpg';

function Camera() {
  const maleImages = ["male1", "male1"];
  const femaleImages = ["female1", "female1"];
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const navigate = useNavigate();
  const [flash, setFlash] = useState(false);
  const [gender, setGender] = useState(null);
  const [isGender, setIsGender] = useState("");
  const [isStarted, setIsStarted] = useState(true);
  const [capturedImage, setCapturedImage] = useState(null);
  const [isGenderShow, setIsGenderShow] = useState(false);
  const [isOptions, setIsOptions] = useState(false);
  const [isImg, setIsImg] = useState(false);
  const [userDetails, setUserDetails] = useState({
    name: "",
    email: "",
    phoneNumber: "",
  });
  const [selectedOption, setSelectedOption] = useState(null);
  const [selectedTheme, setSelectedTheme] = useState(null);
  const [showScene, setShowScene] = useState(false);
  const [imageFolder, setImageFolder] = useState(null);
  const [isThemeSelected, setIsThemeSelected] = useState(false);
  const [showWarning, setShowWarning] = useState(false);
  const camera = "/camera.png";
  const submit = "/submit.png";
  const themes = [
    { id: 1, name: "Red Carpet", image: redcarpet },
    { id: 2, name: "Outer Space", image: outerspace },
    { id: 3, name: "Futuristic", image: Futuristic },
  ];

  const startProcess = (selectedGender) => {
    console.log(selectedGender);
    userDetails.gender = selectedGender;
    setIsStarted(false);
    setIsGenderShow(false);
    setIsGender(selectedGender);
    setGender(selectedOption);
    console.log(selectedOption, selectedGender);
    setSelectedOption(null);
  };

  useEffect(() => {
    if (isCameraOn) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          videoRef.current.srcObject = stream;
        })
        .catch((err) => {
          console.error("error:", err);
          setIsCameraOn(false);
        });
    } else {
      if (videoRef.current && videoRef.current.srcObject) {
        let tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach((track) => track.stop());
      }
    }

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        let tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach((track) => track.stop());
      }
    };
  }, [isCameraOn]);

  const captureImage = () => {
    setTimeout(() => {
      const canvas = canvasRef.current;
      const context = canvas.getContext("2d");
      const video = videoRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
      canvas.toBlob((blob) => {
        const imageUrl = URL.createObjectURL(blob);
        console.log("Captured Image URL:", imageUrl);
        setCapturedImage(imageUrl);
        setIsCameraOn(false);
      }, "image/jpeg");
    }, 500);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserDetails((prevDetails) => ({
      ...prevDetails,
      [name]: value,
    }));
    setShowWarning(false);
  };

  const handleSubmit = (e) => {
    console.log("here");
    e.preventDefault();
    if (!userDetails.name || !userDetails.email || !userDetails.phoneNumber) {
      setShowWarning(true);
    } else {
      setIsGenderShow(true);
      setIsStarted(false);
      console.log(userDetails, "userDetails");
    }
  };

  const handleSelection = (option) => {
    setSelectedOption(option);
  };

  const handleThemeSelect = (theme) => {
    console.log("htemmmmmmee", theme);
    setSelectedTheme(theme);
    setIsThemeSelected(true);
    setIsGenderShow(false);
    setShowScene(true);
    console.log(`theeme, ${theme.name.toLowerCase().replace(" ", "")}`);

    setImageFolder(`${theme.name.toLowerCase().replace(" ", "")}/${userDetails.gender}`);

    console.log("folder for theme", imageFolder);
  };

  const scenes = imageFolder ? [...Array(5).keys()].map((i) => `${imageFolder}/${i + 1}.png`) : [];

  const handleSceneSelection = (scene) => {
    setSelectedOption(scene);
    setIsImg(scene);
    setIsCameraOn(true);
    setShowScene(false);
  };

  function handleRetake() {
    setCapturedImage(null);
    setIsCameraOn(true);
  }

  function handleSubmitImage() {
    navigate("/swap", {
      state: { sourceImage: capturedImage, userDetails, selectedImage: isImg },
    });
  }

  return (
    <section
      className="text-center w-screen h-screen"
      style={{
        backgroundColor: "transparent",  // Default transparent background
      }}
    >
      {isStarted && (
        <div
          className="flex flex-col gap-5 w-full h-full rounded-lg items-center justify-center"
          style={{
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        >
          <StyledInput
            type="text"
            name="name"
            placeholder="Enter name"
            value={userDetails.name}
            onChange={handleChange}
            required
          />

          <StyledInput
            type="email"
            name="email"
            placeholder="Enter email"
            value={userDetails.email}
            onChange={handleChange}
            required
          />

          <StyledInput
            type="tel"
            name="phoneNumber"
            placeholder="Enter phone number"
            value={userDetails.phoneNumber}
            onChange={handleChange}
            required
          />

          <SubmitButton
            onClick={handleSubmit}
            className="w-[428px] h-[104px] cursor-pointer border-none transition-colors  mt-10"
            style={{ marginTop: "40px" }}
          />

          {showWarning && (
            <div className="text-red-500 text-4xl mt-4">Please enter all details.</div>
          )}
        </div>
      )}

      {isGenderShow && (
        <div className="text-center w-screen h-screen flex flex-col items-center justify-center bg-no-repeat">
          <div className="text-6xl font-semibold text-white tracking-wide mb-4">Select Gender</div>

          <div className="flex flex-col justify-center gap-5 mt-6">
            <button
              className="rounded-lg bg-cover bg-center bg-no-repeat w-[298px] h-[291px] border-none cursor-pointer bg-transparent transition-shadow duration-300"
              style={{ backgroundImage: `url(${male})` }}
              onClick={(e) => {
                e.target.classList.add("shadow-[0px_0px_19px_16px_rgba(255,255,255,0.5)]");
                setTimeout(() => startProcess("male"), 500);
              }}
            ></button>

            <button
              className="rounded-lg bg-cover bg-center bg-no-repeat w-[298px] h-[291px] border-none cursor-pointer bg-transparent transition-shadow duration-300"
              style={{ backgroundImage: `url(${female})` }}
              onClick={(e) => {
                e.target.classList.add("shadow-[0px_0px_19px_16px_rgba(255,255,255,0.5)]");
                setTimeout(() => startProcess("female"), 500);
              }}
            ></button>
          </div>
        </div>
      )}

      {/* Show ThemeSlider only if theme is not selected and showScene is false */}
      {isGender && !isThemeSelected && !showScene && (
        <ThemeSlider themes={themes} onSelect={handleThemeSelect} />
      )}

      {isCameraOn && (
        <div className="text-center w-screen h-screen flex flex-col justify-center items-center bg-no-repeat">
          <div className="text-center text-6xl font-semibold mb-2 text-white">Smile for the</div>
          <div className="text-center text-6xl font-semibold mb-8 text-white">camera</div>
          <video
            ref={videoRef}
            autoPlay
            className="block shadow-md object-cover w-full h-full max-w-[650px] max-h-[650px]"
          ></video>

          <canvas ref={canvasRef} className="hidden"></canvas>
          <button
            onClick={(e) => {
              setTimeout(captureImage, 500);
            }}
            className="w-[194px] h-[194px] cursor-pointer  absolute top-[73%]"
          >
            <img src={camera} alt="Capture" style={{ width: "100%", height: "100%", objectFit: "contain" }} />
          </button>
        </div>
      )}

      {capturedImage && (
        <div className="text-center w-screen h-screen flex flex-col justify-center items-center bg-no-repeat">
          <div className="text-center text-6xl font-semibold mb-8 text-white">Preview</div>
          <img src={capturedImage} alt="Captured" style={{ maxWidth: "650px", maxHeight: "650px" }} />
          <div className="flex justify-center mt-8 w-[650px]">
            <SubmitButton onClick={handleRetake} className="mr-4 w-[300px] h-[104px]" style={{ marginTop: "0px" }}>Retake</SubmitButton>
            <SubmitButton onClick={handleSubmitImage} className="w-[300px] h-[104px]" style={{ marginTop: "0px" }}>Submit</SubmitButton>
          </div>
        </div>
      )}

      {showScene && (
        <SceneSlider scenes={scenes} onSelect={handleSceneSelection} />
      )}
    </section>
  );
}

export default Camera;

</file_content>

<file_content path="projects/photobooth/src/Error.jsx">
// eslint-disable-next-line no-unused-vars
import { useNavigate } from "react-router-dom";
function Error() {
    const navigate = useNavigate();
  return (
    <div style={{
      backgroundColor:'#f4fc3f',
        width: "100vw",
        height: "100vh",
        display: "flex",
        flexDirection:'column',
        justifyContent: "center",
        alignItems: "center",
      }}>
     <div style={{textAlign:'center', padding:'30px',backgroundColor:'#f20c3f'}}>
     <h1 >Error something went wrong!</h1>
     <button style={{backgroundColor:'black', color:'white', padding:'10px 25px', border:'none',borderRadius:'5px'}} onClick={()=> navigate("/") }>GO HOME</button>
     </div>
    </div>
  );
}

export default Error;

</file_content>

<file_content path="projects/photobooth/src/index.css">
@import "tailwindcss";

@plugin "tailwindcss-animate";

@custom-variant dark (&:is(.dark *));

:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --destructive-foreground: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.87 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --radius: 0.625rem;
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.87 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.145 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.145 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.396 0.141 25.723);
  --destructive-foreground: oklch(0.637 0.237 25.331);
  --border: oklch(0.269 0 0);
  --input: oklch(0.269 0 0);
  --ring: oklch(0.439 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(0.269 0 0);
  --sidebar-ring: oklch(0.439 0 0);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
}

@layer base {
  * {
    @apply border-border outline-ring/50;
  }
  body {
    @apply bg-background text-foreground;
    background-image: url('/login.png');
    background-size: cover; /* or contain, depending on your preference */
    background-repeat: no-repeat;
  }
}

</file_content>

<file_content path="projects/photobooth/src/LoadingPage.jsx">
// eslint-disable-next-line no-unused-vars
import React from 'react';
import styled, { keyframes } from 'styled-components';

const rotation = keyframes`
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
`;

const rotationBack = keyframes`
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(-360deg);
  }
`;

const LoaderWrapper = styled.div`
  width: 200px; /* Increased size */
  height: 200px; /* Increased size */
  border: 16px dotted #FFF; /* Increased size */
  border-style: solid solid dotted dotted;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  box-sizing: border-box;
  animation: ${rotation} 2s linear infinite;
`;

const LoaderInner = styled.div`
  content: '';  
  box-sizing: border-box;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  margin: auto;
  border: 16px dotted #30A6EC; /* Increased size */
  border-style: solid solid dotted;
  width: 100px; /* Increased size */
  height: 100px; /* Increased size */
  border-radius: 50%;
  animation: ${rotationBack} .5s linear infinite;
  transform-origin: center center;
`;



function LoadingPage() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100vh', width: '100vw' }}>
      <LoaderWrapper>
        <LoaderInner />
      </LoaderWrapper>
    </div>
  );
}

export default LoadingPage;

</file_content>

<file_content path="projects/photobooth/src/main.jsx">
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'

createRoot(document.getElementById('root')).render(
  <>
    <App />
  </>,
)

</file_content>

<file_content path="projects/photobooth/src/Result.jsx">
// import { QRCodeSVG } from 'qrcode.react';
import { forwardRef, useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

// Forward ref for the component to print
const PrintableImage = forwardRef(({ resultImageUrl }, ref) => {
  return (
    <div ref={ref}>
      <img
        src={resultImageUrl}
        alt="Swapped Result"
        style={{ width: "100%", height: "100%" }}
      />
    </div>
  );
});

function Result() {
  const location = useLocation();
  //const { resultImageUrl } = location.state; // Retrieve the image URL passed from Page2
  const { resultImageUrl } = 'https://fuhqxfbyvrklxggecynt.supabase.co/storage/v1/object/public/nimhans/swapped-images/1740378112464-result.jpg'; // Retrieve the image URL passed from Page2
  const navigate = useNavigate();
  const [imageLoaded, setImageLoaded] = useState(false);
  const printRef = useRef(); // Ref for the printable component

  useEffect(() => {
    if (resultImageUrl) {
      const img = new Image();
      img.onload = () => {
        setImageLoaded(true);
      };
      img.src = resultImageUrl;
    }
  }, [resultImageUrl]);

  const goHome = () => {
    navigate("/");
  };

  return (
    <div>
      {resultImageUrl ? (
        <div
          style={{
            textAlign: "center",
            width: "100vw",
            height: "100vh",
            display: "flex",
            flexDirection: "column",
            justifyContent: "flex-end",
            alignItems: "center",
          }}
        >
          <img
            className="animate__animated animate__fadeIn animate__slower"
            src={resultImageUrl}
            alt="Swapped Result"
            style={{
              width: "788px",
              height: "1042px",
              objectFit: "cover",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              borderRadius: "16px",
              border: "12px solid #FFCE00",
            
            }}
          />
          {imageLoaded && (
            <div
              style={{
                width: "70%",
                height: "25%",
                display: "flex",
                alignItems: "center",
              }}
            >
              <div
                style={{
                  width: "50%",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "flex-start",
                }}
              >
                {/* <QRCodeSVG
                  value={resultImageUrl}
                  size={300}
                  style={{
                    border: "20px solid #30A6EC",
                    borderRadius: "16px",
                    padding: "15px",
                    backgroundColor: "#fff",
                  }}
                /> */}
              </div>

              <div
                style={{
                  width: "35%",
                  marginLeft: "100px",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "flex-start",
                }}
              >
                <div
                  style={{
                    color: "#fff",
                    textAlign: "left",
                    backgroundColor: "rgb(0 29 131)",
                  }}
                >
                  <h1 style={{ fontSize: "42px", lineHeight: "40px" }}>
                    {" "}
                    Scan and Download
                  </h1>
                  <h1
                    style={{
                      fontSize: "20px",
                      lineHeight: "25px",
                      marginTop: "-16px",
                    }}
                  >
                    your warrior alter ego.
                  </h1>
                </div>
                    

              

                <button
                  type="submit"
                  style={{
                    width: "250px",
                    height: "80px",
                    cursor: "pointer",
                    borderRadius: "10px",
                    border: "none",
                    fontSize: "40px",
                    fontWeight: "bold",
                    backgroundColor: "#ffffff", // Default color
                    color: "#000000", // Default text color
                    transition: "background-color 0.3s ease, color 0.3s ease",
                  }}
                  onClick={(e) => {
                    e.target.style.backgroundColor = "#30A6EC"; // Change background
                    e.target.style.color = "#ffffff"; // Change text color
                    setTimeout(goHome, 500); // Correctly invoke captureImage after 500ms
                  }}
                >
                  Restart
                </button>
              </div>
            </div>
          )}
        </div>
      ) : (
        <p>No image found. Please go back and try again.</p>
      )}
    </div>
  );
}

export default Result;

</file_content>

<file_content path="projects/photobooth/src/SceneSlider.jsx">
import { cn } from "@/lib/utils";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useState } from 'react';

const SceneSlider = ({ scenes, onSelect }) => {
  const [activeIndex, setActiveIndex] = useState(0);
  console.log(scenes.length);

  const nextSlide = () => {
    setActiveIndex((prev) => (prev === scenes.length - 1 ? 0 : prev + 1));
  };

  const prevSlide = () => {
    setActiveIndex((prev) => (prev === 0 ? scenes.length - 1 : prev - 1));
  };

  const goToSlide = (index) => {
    setActiveIndex(index);
  };

  const handleSceneSelect = () => {
    onSelect(scenes[activeIndex]);
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="mb-8 text-center">
        <h1 className="mb-2 text-7xl font-bold text-pink-400">Select your scene or background</h1>
      </div>

      <div className="relative flex items-center justify-center px-20">
        {/* Navigation Buttons */}
        <button
          onClick={prevSlide}
          className="absolute -left-32 z-10 rounded-full bg-pink-400 p-2 text-white transition-colors hover:bg-pink-300 shadow-lg"
          aria-label="Previous slide"
        >
          <ChevronLeft className="h-16 w-16" />
        </button>

        {/* Slides */}
        <div className="relative h-[750px] w-[450px]">
          {scenes.map((scene, index) => {
            // Calculate position relative to active slide
            const position = index - activeIndex;

            return (
              <div
                key={scene}
                className={cn("absolute left-0 top-0 h-full w-full transition-all duration-300 ease-in-out", {
                  "z-30 scale-100 rotate-0": position === 0,
                  "z-20 -translate-x-[30%] scale-80 rotate-[-10deg]": position === -1 || position === 2,
                  "z-10 translate-x-[30%] scale-80 rotate-[10deg]": position === 1 || position === -2,
                })}
              >
                <div className="relative h-full w-full overflow-hidden rounded-3xl border-4 border-pink-400 bg-gray-900 shadow-xl">
                  <img
                    onClick={handleSceneSelect}
                    src={scene}
                    alt={`Scene ${index + 1}`}
                    className="h-full w-full object-cover"
                  />
                </div>
              </div>
            );
          })}
        </div>

        {/* Next Button */}
        <button
          onClick={nextSlide}
          className="absolute -right-32 z-10 rounded-full bg-pink-400 p-2 text-pink-600 transition-colors hover:bg-pink-300 shadow-lg"
          aria-label="Next slide"
        >
          <ChevronRight className="h-16 w-16" />
        </button>
      </div>

      {/* Dots */}
      <div className="mt-8 flex gap-2">
        {scenes.map((_, index) => (
          <button
            key={index}
            onClick={() => goToSlide(index)}
            className={cn(
              "h-3 w-3 rounded-full transition-colors",
              activeIndex === index ? "bg-pink-400" : "bg-white opacity-50 hover:opacity-75"
            )}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>

      {/* Scene Name */}
      {scenes[activeIndex] && (
        <div className="mt-8 rounded-lg bg-pink-400 px-6 py-2">
          <span className="text-xl font-bold uppercase text-pink-600">
            {scenes[activeIndex].split('/').pop().split('.')[0]}
          </span>
        </div>
      )}
    </div>
  );
};

export default SceneSlider;
</file_content>

<file_content path="projects/photobooth/src/supabaseClient.js">
// supabaseClient.js
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://fuhqxfbyvrklxggecynt.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1aHF4ZmJ5dnJrbHhnZ2VjeW50Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4ODk0MzcsImV4cCI6MjA1MzQ2NTQzN30.0r2cHr8g6nNwjaVaVGuXjo9MXNFu9_rx40j5Bb3Ib2Q';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

</file_content>

<file_content path="projects/photobooth/src/Swap.jsx">
// eslint-disable no-unused-vars
import { QRCodeSVG } from "qrcode.react";
import { forwardRef, useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { ReactToPrint } from "react-to-print";
import LoadingPage from "./LoadingPage";
import { supabase } from "./supabaseClient";

function Swap() {
  const navigate = useNavigate();
  const location = useLocation();
  const sourceImageBlob = location.state?.sourceImage;
  const selectedImage = location.state?.selectedImage;
  const userDetails = location.state?.userDetails;
  const [loading, setLoading] = useState(false);
  const [resultImageUrl, setResultImageUrl] = useState(null);
  const [error, setError] = useState(null);
  const printRef = useRef();
  const [isPrint, setPrint] = useState(true);
  const [horizontal, setHorizontal] = useState(false); // New state for layout control

const dummyimge='https://fuhqxfbyvrklxggecynt.supabase.co/storage/v1/object/public/nimhans/swapped-images/1740573041166-result.jpg'
console.log("dummyimge",dummyimge);
  useEffect(() => {
    // Check if we have the required data
    if (!sourceImageBlob || !selectedImage || !userDetails) {
      console.error("Missing required data:", { sourceImageBlob, selectedImage, userDetails });
      navigate("/");
      return;
    }
    const LoadingAnimation = () => {
      return (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
            width: "100vw",
          }}
        >
          <LoaderContainer>
            <Bar color="rgb(255 255 255)" delay={0.3} /> {/* Blue */}
            <Bar color="rgb(255 255 255)" delay={0.2} /> {/* Green */}
            <Bar color="rgb(255 255 255)" delay={0.1} /> {/* Yellow */}
            <Bar color="rgb(255 255 255)" delay={0} /> {/* Red */}
          </LoaderContainer>
        </div>
      );
    };
    const processImages = async () => {
      setLoading(true);
      try {
        // Create FormData
        const formData = new FormData();
        formData.append(
          "targetImage",
          new File([sourceImageBlob], "sourceImage.jpg", { type: "image/jpeg" })
        );

        // Fetch the selected image and append it
        const response = await fetch(selectedImage);
        if (!response.ok) throw new Error("Failed to fetch selected image");
        
        const targetImageBlob = await response.blob();
        formData.append(
          "sourceImage",
          new File([targetImageBlob], "targetImage.jpg", { type: "image/jpeg" })
        );

        // Add user details
        formData.append("name", userDetails.name);
        formData.append("email", userDetails.email);

        // Make API call to swap faces
        const swapResponse = await fetch(
          "https://api.nodeshed.com/api/swap-face/",
          {
            method: "POST",
            body: formData,
          }
        );

        if (!swapResponse.ok) {
          throw new Error(`Swap API error: ${swapResponse.statusText}`);
        }

        const swappedImageBlob = await swapResponse.blob();
        const convertedBlob = await convertImageToJPEG(swappedImageBlob);
       const foldername='swapped-images'
        // Generate filename with timestamp
        const fileName = `${foldername}/${Date.now()}-result.jpg`;

        // Upload to Supabase
        const { error: uploadError } = await supabase.storage
          .from("nimhans")
          .upload(fileName, convertedBlob, {
            contentType: "image/jpeg",
          });

        if (uploadError) throw uploadError;

        // Get public URL
        const publicURL = `https://fuhqxfbyvrklxggecynt.supabase.co/storage/v1/object/public/nimhans/${fileName}`;
        console.log("Public URL:", publicURL);

        // // Save user details to database
        const { error: insertError } = await supabase
          .from("nimhans")
          .insert([{ ...userDetails, publicURL }]);

        if (insertError) throw insertError;

        setResultImageUrl(publicURL);
      } catch (err) {
        console.error("Error processing images:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    processImages();
  }, []); // Empty dependency array since we want this to run once on mount


  // Helper function to convert image to JPEG
  const convertImageToJPEG = (blob) => {
    return new Promise((resolve, reject) => {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      const img = new Image();

      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        canvas.toBlob(resolve, "image/jpeg");
      };

      img.onerror = reject;
      img.src = URL.createObjectURL(blob);
    });
  };

  // Create a PrintableImage component using forwardRef
  const PrintableImage = forwardRef(({ resultImageUrl }, ref) => {
    return (
      <div ref={ref}>
        <img src={resultImageUrl} alt="Swapped Result" style={{ width: "100%", height: "100%" }} />
      </div>
    );
  });

  // Handle navigation back to home
  const goHome = () => {
    navigate("/");
  };

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <div className="bg-red-500 p-16 rounded-lg shadow-lg text-center">
          <div className="text-white text-3xl mb-4">Something went wrong: {error}</div>
          <button
            onClick={goHome}
            className="bg-white text-3xl  text-blue-900 px-12 py-4 rounded font-bold"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <LoadingPage />
      </div>
    );
  }

  if (resultImageUrl) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4">
        <div className="w-full max-w-4xl mt-8 p-8">
          <div className="flex justify-between items-center ">
            <div className="text-3xl text-white">&nbsp;</div> {/* Keeps the spacing */}
          </div>

          {horizontal ? (
            <div className="flex flex-row items-center justify-between gap-8">
              {/* Increased image size in horizontal layout */}
              <div className="w-full">
                <img
                  src={resultImageUrl}
                  alt="Swapped Result"
                  className="w-full animate__animated animate__zoomIn"
                />
              </div>
              <div className="w-1/3 flex flex-col items-center">
                <div className="bg-white p-4 border-12 border-yellow-400">
                  <QRCodeSVG value={resultImageUrl} size={180} />
                </div>
                <div className="text-white flex flex-col items-center mt-8">
                  <h1 className="text-3xl mb-4 font-semibold text-center">Scan the QR <br/> code to download<br/> your AI avatar</h1>
                  {isPrint ? (
                    <div className="flex flex-col gap-4">
                      <ReactToPrint
                        trigger={() => (
                          <button
                            type="button"
                            className="bg-yellow-400 text-black px-8 py-4 text-4xl font-bold rounded-lg w-full"
                          >
                            Print
                          </button>
                        )}
                        content={() => printRef.current}
                      />

                      <button
                        onClick={goHome}
                        className="bg-yellow-400 text-black px-8 py-4 text-4xl font-bold rounded-lg w-full"
                      >
                        RESTART
                      </button>

                      <div style={{ display: "none" }}>
                        <PrintableImage
                          ref={printRef}
                          resultImageUrl={resultImageUrl}
                        />
                      </div>
                    </div>
                  ) : null}
                </div>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <img
                src={resultImageUrl}
                alt="Swapped Result"
                className="w-full animate__animated animate__zoomIn p-20"
              />
              <div className="flex justify-start items-center mt-8 px-20">
                <div className="bg-white p-4 border-12 border-yellow-400">
                  <QRCodeSVG value={resultImageUrl} size={180} />
                </div>
                <div className="text-white flex flex-col ml-40">
                  <h1 className="text-3xl mb-4 font-semibold text-left">Scan the QR <br/> code to download<br/> your AI avatar</h1>
                  {isPrint ? (
                    <div className="flex flex-col gap-4">
                      <ReactToPrint
                        trigger={() => (
                          <button
                            type="button"
                            className="bg-yellow-400 text-black px-8 py-4 text-4xl font-bold rounded-lg"
                          >
                            Print
                          </button>
                        )}
                        content={() => printRef.current}
                      />

                      <button
                        onClick={goHome}
                        className="bg-yellow-400 text-black px-8 py-4 text-4xl font-bold rounded-lg"
                      >
                        RESTART
                      </button>

                      <div style={{ display: "none" }}>
                        <PrintableImage
                          ref={printRef}
                          resultImageUrl={resultImageUrl}
                        />
                      </div>
                    </div>
                  ) : null}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return null;
}

export default Swap;
</file_content>

<file_content path="projects/photobooth/src/theme-slider.jsx">
import { cn } from "@/lib/utils"
import { ChevronLeft, ChevronRight } from "lucide-react"
import * as React from "react"

export function ThemeSlider({ themes, onSelect }) {
  const [activeIndex, setActiveIndex] = React.useState(0)

  const nextSlide = () => {
    setActiveIndex((prev) => (prev === themes.length - 1 ? 0 : prev + 1))
  }

  const prevSlide = () => {
    setActiveIndex((prev) => (prev === 0 ? themes.length - 1 : prev - 1))
  }

  const goToSlide = (index) => {
    setActiveIndex(index)
  }

  const handleThemeSelect = () => {
    onSelect(themes[activeIndex])
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="mb-8 text-center">
        <h1 className="mb-2 text-7xl font-bold text-white">Select your theme</h1>
      </div>

      <div className="relative flex items-center justify-center px-20">
        {/* Navigation Buttons */}
        <button
          onClick={prevSlide}
          className="absolute -left-32 z-10 rounded-full bg-sky-950 p-2 text-white transition-colors hover:bg-sky-800 shadow-lg"
          aria-label="Previous slide"
        >
          <ChevronLeft className="h-16 w-16" />
        </button>

        <div className="relative h-[750px] w-[450px]">
          {themes.map((theme, index) => {
            // Calculate position relative to active slide
            const position = index - activeIndex

            return (
              <div
                key={theme.id}
                className={cn("absolute left-0 top-0 h-full w-full transition-all duration-300 ease-in-out", {
                  "z-30 scale-100 rotate-0": position === 0,
                  "z-20 -translate-x-[30%] scale-80 rotate-[-10deg]": position === -1 || position === 2,
                  "z-10 translate-x-[30%] scale-80 rotate-[10deg]": position === 1 || position === -2,
                })}
              >
                <div className="relative h-full w-full overflow-hidden ">
                  <img
                    onClick={handleThemeSelect}
                    src={theme.image || "/placeholder.svg"}
                    alt={theme.name}
                    className="h-full w-full object-cover"
                  />
                </div>
              </div>
            )
          })}
        </div>

        {/* Next Button */}
        <button
          onClick={nextSlide}
          className="absolute -right-32 z-10 rounded-full bg-sky-950 p-2 text-white transition-colors hover:bg-sky-800 shadow-lg"
          aria-label="Next slide"
        >
          <ChevronRight className="h-16 w-16" />
        </button>
      </div>

      {/* Dots */}
      <div className="mt-8 flex gap-2">
        {themes.map((_, index) => (
          <button
            key={index}
            onClick={() => goToSlide(index)}
            className={cn(
              "h-3 w-3 rounded-full transition-colors",
              activeIndex === index ? "bg-sky-950" : "bg-white opacity-50 hover:opacity-75",
            )}
            aria-label={`Go to slide ${index + 1}`}
          >
            <span style={{ color: 'white' }}></span>
          </button>
        ))}
      </div>

      {/* Theme Name */}
      <div className="mt-8 rounded-lg bg-sky-950 px-12 py-4">
        <span className="text-3xl font-bold uppercase text-white">{themes[activeIndex].name}</span>
      </div>
    </div>
  )
}
</file_content>
</folder_content>

<environment_details>
# VSCode Visible Files
C:/Users/rahul/AppData/Local/Programs/Microsoft VS Code/projects/photobooth/src/Camera.jsx
C:/Users/rahul/AppData/Local/Programs/Microsoft VS Code/projects/photobooth/src/Camera.jsx
react-lmstudio.py

# VSCode Open Tabs
.env
c:/Users/rahul/AppData/Roaming/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
projects/photobooth/src/Camera.jsx
projects/photobooth/src/Swap.jsx
react-lmstudio.py

# Current Time
3/22/2025, 12:22:19 PM (Asia/Calcutta, UTC+5.5:00)

# Current Working Directory (d:/crew) Files
.gitignore
a
app.py
changes copy.json
changes.json
coding_agent.py
crew_ollama.py
crewai_agent.py
crewai_agent2.py
crewgroq.py
gitignore
justreact_improver.py
lmstudio.py
react_crew_groq.py
react_improver_cohere.py
react_improver.py
react_improvereditfile.py
react_latest.py
react-latest-with-reviewer.py
react-lmstudio.py
readme.md
test.py
test2.py
testollam.py
input/
input/src/
input/src/Camera.jsx
input/src/userForm.jsx
output/
projects/
projects/photobooth/
projects/photobooth/.gitignore
projects/photobooth/components.json
projects/photobooth/eslint.config.js
projects/photobooth/index.html
projects/photobooth/jsconfig.json
projects/photobooth/package.json
projects/photobooth/README.md
projects/photobooth/start.bat
projects/photobooth/vite.config.js
projects/photobooth/yarn.lock
projects/photobooth/public/
projects/photobooth/public/background.jpg
projects/photobooth/public/background2.jpg
projects/photobooth/public/camera.png
projects/photobooth/public/f1.jpeg
projects/photobooth/public/f1.jpg
projects/photobooth/public/f2.jpeg
projects/photobooth/public/f2.jpg
projects/photobooth/public/f3.jpeg
projects/photobooth/public/f4.jpeg
projects/photobooth/public/f5.jpeg
projects/photobooth/public/female.jpg
projects/photobooth/public/firstImg.png
projects/photobooth/public/Futuristic.png
projects/photobooth/public/Futuristicm.png
projects/photobooth/public/glamour.png
projects/photobooth/public/hoves.otf
projects/photobooth/public/lf.png
projects/photobooth/public/lm.png
projects/photobooth/public/Login1.png
projects/photobooth/public/london.png
projects/photobooth/public/m1.jpeg
projects/photobooth/public/m1.jpg
projects/photobooth/public/m2.jpeg
projects/photobooth/public/m2.jpg
projects/photobooth/public/m3.jpeg
projects/photobooth/public/m4.jpeg
projects/photobooth/public/m5.jpeg
projects/photobooth/public/male.jpg
projects/photobooth/public/newyork.png
projects/photobooth/public/nf.png
projects/photobooth/public/nm.png
projects/photobooth/public/nyc.png
projects/photobooth/public/outerspace.png
projects/photobooth/public/paris.png
projects/photobooth/public/PayPal.ttf
projects/photobooth/public/pf.png
projects/photobooth/public/pm.png
projects/photobooth/public/redcarpet.png
projects/photobooth/public/sattvaBg.png
projects/photobooth/public/scifi.png
projects/photobooth/public/sf.png
projects/photobooth/public/sm.png
projects/photobooth/public/sports.png
projects/photobooth/public/submit.png
projects/photobooth/public/swi.png
projects/photobooth/public/tf.png
projects/photobooth/public/tm.png
projects/photobooth/public/tok.png
projects/photobooth/public/tokyo.png
projects/photobooth/public/toronto.png
projects/photobooth/public/underwater.png
projects/photobooth/public/assets/
projects/photobooth/public/assets/bb.gif
projects/photobooth/public/assets/bg.png
projects/photobooth/public/assets/bg00.png
projects/photobooth/public/assets/bg01.png
projects/photobooth/public/assets/bg02.png
projects/photobooth/public/assets/bg03.png
projects/photobooth/public/assets/bg04.png
projects/photobooth/public/assets/bg05.png
projects/photobooth/public/assets/button.png
projects/photobooth/public/assets/capture.png
projects/photobooth/public/assets/capturegg.png
projects/photobooth/public/assets/capturer.png
projects/photobooth/public/assets/cft.png
projects/photobooth/public/assets/couple.png
projects/photobooth/public/assets/cp.png
projects/photobooth/public/assets/dd.png
projects/photobooth/public/assets/dell.png
projects/photobooth/public/assets/ex.png
projects/photobooth/public/assets/exbt.png
projects/photobooth/public/assets/excp.png
projects/photobooth/public/assets/exotel.png
projects/photobooth/public/assets/f1.jpg
projects/photobooth/public/assets/f1.png
projects/photobooth/public/assets/f2.jpg
projects/photobooth/public/assets/f2.png
projects/photobooth/public/assets/female.png
projects/photobooth/public/assets/Frame 1 (1).png
projects/photobooth/public/assets/intel.png
projects/photobooth/public/assets/Loading.gif
projects/photobooth/public/assets/m1.png
projects/photobooth/public/assets/m2.png
projects/photobooth/public/assets/male.png
projects/photobooth/public/assets/Mask group (3).png
projects/photobooth/public/assets/Mask group (4).png
projects/photobooth/public/assets/mask.png
projects/photobooth/public/assets/one.png
projects/photobooth/public/assets/palo.png
projects/photobooth/public/assets/pcp.png
projects/photobooth/public/assets/pmagic.png
projects/photobooth/public/assets/pst.png
projects/photobooth/public/assets/reset_btn.png
projects/photobooth/public/assets/sentinel.png
projects/photobooth/public/assets/startbg.png
projects/photobooth/public/assets/two.png
projects/photobooth/public/assets/wizcraft.jpg
projects/photobooth/public/futuristic/
projects/photobooth/public/futuristic/female/
projects/photobooth/public/futuristic/female/1.png
projects/photobooth/public/futuristic/female/2.png
projects/photobooth/public/futuristic/female/3.png
projects/photobooth/public/futuristic/male/
projects/photobooth/public/futuristic/male/1.png
projects/photobooth/public/futuristic/male/2.png
projects/photobooth/public/futuristic/male/3.png
projects/photobooth/public/outerspace/
projects/photobooth/public/outerspace/female/
projects/photobooth/public/outerspace/female/1.png
projects/photobooth/public/outerspace/female/2.png
projects/photobooth/public/outerspace/female/3.png
projects/photobooth/public/outerspace/male/
projects/photobooth/public/outerspace/male/1.png
projects/photobooth/public/outerspace/male/2.png
projects/photobooth/public/outerspace/male/3 copy.png
projects/photobooth/public/outerspace/male/3.png
projects/photobooth/public/outerspace/male/4.png
projects/photobooth/public/outerspace/male/5.png
projects/photobooth/public/redcarpet/
projects/photobooth/public/redcarpet/female/
projects/photobooth/public/redcarpet/female/1.png
projects/photobooth/public/redcarpet/female/2.png
projects/photobooth/public/redcarpet/female/3.png
projects/photobooth/public/redcarpet/male/
projects/photobooth/public/redcarpet/male/1.png
projects/photobooth/public/redcarpet/male/2.png
projects/photobooth/public/redcarpet/male/3.png
projects/photobooth/public/sports/
projects/photobooth/public/sports/female/
projects/photobooth/public/sports/female/1.png
projects/photobooth/public/sports/female/2.png
projects/photobooth/public/sports/female/3.png
projects/photobooth/public/sports/female/4.png
projects/photobooth/public/sports/female/5.png
projects/photobooth/public/sports/male/
projects/photobooth/public/sports/male/1.png
projects/photobooth/public/sports/male/2.png
projects/photobooth/public/sports/male/3.png
projects/photobooth/public/underwater/
projects/photobooth/public/underwater/female/
projects/photobooth/public/underwater/male/
projects/photobooth/src/
projects/photobooth/src/App.css
projects/photobooth/src/App.jsx
projects/photobooth/src/Camera.jsx
projects/photobooth/src/Error.jsx
projects/photobooth/src/index.css
projects/photobooth/src/LoadingPage.jsx
projects/photobooth/src/main.jsx
projects/photobooth/src/Result.jsx
projects/photobooth/src/SceneSlider.jsx
projects/photobooth/src/supabaseClient.js
projects/photobooth/src/Swap.jsx
projects/photobooth/src/theme-slider.jsx
projects/photobooth/src/assets/
projects/photobooth/src/assets/react.svg
projects/photobooth/src/lib/
projects/photobooth/src/lib/utils.js

(File list truncated. Use list_files on specific subdirectories if you need to explore further.)

# Current Mode
ACT MODE
</environment_details>