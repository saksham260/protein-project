"use client";

import React from "react";
import dynamic from "next/dynamic";

const shaderProps: any = {
  animate: "on",
  axesHelper: "off",
  bgColor1: "#F1FDFB",
  bgColor2: "#E6F5F1",
  brightness: 0.98,
  cAzimuthAngle: 180,
  cDistance: 3.6,
  cPolarAngle: 90,
  cameraZoom: 1,
  color1: "#DCEAD9",
  color2: "#F4FBF7",
  color3: "#F1FDFB",
  destination: "onCanvas",
  embedMode: "off",
  envPreset: "city",
  format: "gif",
  fov: 45,
  frameRate: 10,
  gizmoHelper: "hide",
  grain: "off",
  lightType: "3d",
  pixelDensity: 0.8,
  positionX: -1.4,
  positionY: 0,
  positionZ: 0,
  range: "disabled",
  rangeEnd: 40,
  rangeStart: 0,
  reflection: 0.1,
  rotationX: 0,
  rotationY: 10,
  rotationZ: 50,
  shader: "defaults",
  type: "plane",
  uAmplitude: 1,
  uDensity: 1.3,
  uFrequency: 5.5,
  uSpeed: 0.4,
  uStrength: 4,
  uTime: 0,
  wireframe: false,
};

const ShaderCanvas = dynamic(
  () =>
    import("@shadergradient/react").then((mod) => {
      const { ShaderGradientCanvas, ShaderGradient } = mod;
      return function ShaderCanvasInner({ props }: { props: any }) {
        return (
          <ShaderGradientCanvas
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              pointerEvents: "none",
            }}
            pixelDensity={0.8}
            fov={45}
          >
            <ShaderGradient {...props} />
          </ShaderGradientCanvas>
        );
      };
    }),
  { ssr: false }
);

export function BackgroundShader() {
  return null;
}

export default BackgroundShader;
