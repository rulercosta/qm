const CACHE_NAME = 'qm-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/global.css',
  '/static/css/loader.css',
  '/static/js/scriptManager.js',
  '/static/js/router.js',
  '/static/images/icon-192.png',
  '/static/images/icon-512.png',
  '/static/favicon.ico'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
