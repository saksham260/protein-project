"use client";

import React, { useState } from "react";
import Image, { type ImageProps } from "next/image";

/** next/image that shows `fallback` instead of a broken picture when the brand's image is gone or blocked. */
export const ImageWithFallback: React.FC<ImageProps & { fallback: React.ReactNode }> = ({ fallback, alt, ...props }) => {
  const [failedSrc, setFailedSrc] = useState<unknown>(null);
  if (failedSrc === props.src) return <>{fallback}</>;
  return <Image alt={alt} {...props} onError={() => setFailedSrc(props.src)} />;
};
