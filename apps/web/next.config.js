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
        hostname: "www.royalenfield.com",
      },
      {
        protocol: "https",
        hostname: "hondanews.com",
      },
      {
        protocol: "https",
        hostname: "www.honda2wheelersindia.com",
      },
      {
        protocol: "https",
        hostname: "www.heromotocorp.com",
      },
      {
        protocol: "https",
        hostname: "www.bajajauto.com",
      },
      {
        protocol: "https",
        hostname: "www.tvsmotor.com",
      },
      {
        protocol: "https",
        hostname: "www.yamaha-motor-india.com",
      },
      {
        protocol: "https",
        hostname: "www.ktmindia.com",
      },
      {
        protocol: "https",
        hostname: "www.triumphind.in",
      },
      {
        protocol: "https",
        hostname: "placehold.co",
      },
    ],
  },
};

module.exports = nextConfig;
