import React from 'react';
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

const Container = styled.section`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100vw;
  height: 100vh;
  color: white;
  padding: 1rem;
  box-sizing: border-box;
  background-image: url('https://fuhqxfbyvrklxggecynt.supabase.co/storage/v1/object/public/nielsen/backgrounds/1741599792665-bggg.jpg');
  background-size: cover;
  background-position: center;
`;

const Title = styled.h1`
  font-size: clamp(1.5rem, 5vw, 2.5rem);
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: center;
`;

const CameraWrapper = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 650px;
  margin: 0 auto;
`;

const CameraContainer = styled.div`
  position: relative;
  width: 100%;
  max-width: 650px;
  height: auto;
  margin: 0 auto;
  border-radius: 8px;
  overflow: hidden;
`;

const VideoElement = styled.video`
  width: 100%;
  max-width: 650px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  object-fit: cover;
  aspect-ratio: 16/9;
  display: block;
  margin: 0 auto;
`;

const CapturedImage = styled.img`
  width: 100%;
  max-width: 650px;
  height: auto;
  max-height: 650px;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: block;
  margin: 0 auto;
`;

const CaptureButton = styled.button`
  width: 120px;
  height: 120px;
  border: 2px solid black;
  cursor: pointer;
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 50%;
  background-color: red;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  transition: transform 0.3s ease, background-color 0.3s;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  z-index: 10;
  animation: pulse 2s infinite;
  
  &:hover {
    transform: translateX(-50%) scale(1.05);
    background-color: #ffc107;
  }
  
  &:active {
    transform: translateX(-50%) scale(0.95);
  }
  
  @keyframes pulse {
    0% {
      transform: translateX(-50%) scale(1);
    }
    50% {
      transform: translateX(-50%) scale(1.05);
    }
    100% {
      transform: translateX(-50%) scale(1);
    }
  }
`;

const ButtonContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 1.5rem;
  width: 100%;
  max-width: 650px;
`;

const ActionButton = styled.button`
  padding: 16px 32px;
  border: 2px solid black;
  background-color: red;
  color: white;
  border-radius: 8px;
  font-size: 24px;
  cursor: pointer;
  flex: 1;
  max-width: 200px;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: #ffc107;
  }
`;

const RetakeButton = styled(ActionButton)`
/* No additional styles needed */
`;

const SubmitButton = styled(ActionButton)`
/* No additional styles needed */
`;

const ErrorMessage = styled.div`
  color: #ef4444;
  text-align: center;
  margin: 1rem 0;
  padding: 10px;
  border-radius: 8px;
  background-color: rgba(239, 68, 68, 0.1);
  max-width: 650px;
  width: 100%;
`;

function Camera() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();
  const [capturedImage, setCapturedImage] = useState(null);
  const [isCameraOn, setIsCameraOn] = useState(true);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  // Start camera when component mounts or when returning from preview
  useEffect(() => {
    if (isCameraOn) {
      startCamera();
    }
    
    // Cleanup function to stop camera when component unmounts
    return () => {
      stopCamera();
    };
  }, [isCameraOn]);

  // Function to start the camera
  const startCamera = async () => {
    setIsLoading(true);
    setError("");

    try {
      const constraints = { 
        video: {
          facingMode: "user",
          width: { ideal: 650 },
          height: { ideal: 650 }
        } 
      };
      
      const stream = await navigator.mediaDevices.getUserMedia(constraints);

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.onloadedmetadata = () => {
          setIsLoading(false);
        };
      }
    } catch (err) {
      console.error("Camera error:", err);
      setError("Unable to access camera. Please ensure you've granted permission.");
      setIsLoading(false);
    }
  };

  // Function to stop the camera
  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  // Function to capture image
  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;

    if (!canvas || !video) return;

    const context = canvas.getContext("2d");

    // Set canvas dimensions - limit to max 650px while maintaining aspect ratio
    const videoWidth = video.videoWidth;
    const videoHeight = video.videoHeight;

    // Calculate new dimensions while preserving aspect ratio and not exceeding 650px
    let targetWidth = videoWidth;
    let targetHeight = videoHeight;
    
    if (targetWidth > 650) {
      targetWidth = 650;
      targetHeight = (videoHeight / videoWidth) * targetWidth;
    }
    
    if (targetHeight > 650) {
      targetHeight = 650;
      targetWidth = (videoWidth / videoHeight) * targetHeight;
    }
    
    canvas.width = targetWidth;
    canvas.height = targetHeight;

    // Draw video frame to canvas with the calculated dimensions
    context.drawImage(video, 0, 0, targetWidth, targetHeight);

    // Convert canvas to blob
    canvas.toBlob((blob) => {
      if (!blob) {
        setError("Failed to capture image. Please try again.");
        return;
      }
      
      const imageUrl = URL.createObjectURL(blob);
      setCapturedImage(imageUrl);
      setIsCameraOn(false); // Turn off camera
      stopCamera(); // Stop camera stream
      
      // Store blob for later use
      canvas.blob = blob;
    }, "image/jpeg", 0.9);

  };

  // Function to retake photo
  const retakePhoto = () => {
    if (capturedImage) {
      URL.revokeObjectURL(capturedImage); // Clean up the object URL
    }
    setCapturedImage(null);
    setIsCameraOn(true); // Turn camera back on
  };

  // Function to submit photo and navigate to swap page
  const submitPhoto = () => {
    const blob = canvasRef.current.blob;
    if (!blob) {
      setError("Image data not found. Please recapture.");
      return;
    }
    
    navigate("/swap", {
      state: { sourceImageBlob: blob }
    });
  };

  return (
    <Container>
      <Title>{capturedImage ? "Preview" : "Camera"}</Title>

      
      {error && <ErrorMessage>{error}</ErrorMessage>}
      
      <CameraWrapper>
        {isCameraOn && !capturedImage ? (
          <CameraContainer>
            <VideoElement
              ref={videoRef}
              autoPlay
              playsInline
              muted
            />
            {!isLoading && (
              <CaptureButton onClick={captureImage} aria-label="Capture photo">
                Capture
              </CaptureButton>
            )}
            {isLoading && (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                Loading camera...
              </div>
            )}
          </CameraContainer>
        ) : (
          capturedImage && (
            <>
              <CapturedImage
                src={capturedImage}
                alt="Captured"
              />
              
              <ButtonContainer>
                <RetakeButton onClick={retakePhoto} aria-label="Retake photo">
                  Retake
                </RetakeButton>
                <SubmitButton onClick={submitPhoto} aria-label="Submit photo">
                  Submit
                </SubmitButton>
              </ButtonContainer>
            </>
          )
        )}
      </CameraWrapper>

      
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </Container>
  );
}

export default Camera;