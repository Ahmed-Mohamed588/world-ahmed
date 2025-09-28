/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Enable experimental features for better performance
  experimental: {
    appDir: false, // Keep pages router for now
    optimizeCss: true,
    scrollRestoration: true,
  },

  // Image optimization
  images: {
    domains: ['localhost', 'your-domain.com'],
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  // Headers for better performance and security
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN'
          }
        ],
      },
    ]
  },

  // Webpack configuration for better animations
  webpack: (config, { isServer }) => {
    // Add support for GLSL shaders (for Three.js)
    config.module.rules.push({
      test: /\.(glsl|vs|fs|vert|frag)$/,
      type: 'asset/source',
    });

    // Optimize bundle splitting
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };
    }

    return config;
  },

  // Environment variables
  env: {
    CUSTOM_KEY: 'my-value',
  },
}

module.exports = nextConfig