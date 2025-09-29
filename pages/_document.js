import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="ar" dir="ltr">
      <Head>
        {/* Favicon */}
        <link rel="icon" href="/favicon.ico" />
        
        {/* Google Fonts */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link 
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Cairo:wght@300;400;600;700;800&display=swap" 
          rel="stylesheet" 
        />
        
        {/* Meta Tags */}
        <meta name="theme-color" content="#0f172a" />
        <meta name="description" content="Ahmed Mohamed - Full Stack Developer specializing in web development, AI automation, and e-commerce solutions" />
      </Head>
      <body className="antialiased">
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
