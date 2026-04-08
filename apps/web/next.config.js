/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "media.royalenfield.com",
      },
      {
        protocol: "https",
        hostname: "hondanews.com",
      },
    ],
  },
};

module.exports = nextConfig;
