let player;

window.onSpotifyWebPlaybackSDKReady = () => {
    player = new Spotify.Player({
        name: 'Hitster Player',
        getOAuthToken: cb => { cb(accessToken); },
        volume: 0.8
    });

    player.addListener('ready', ({ device_id }) => {
        console.log('Device ready:', device_id);

        const qr = new Html5QrcodeScanner("reader", {
            fps: 10,
            qrbox: 250
        });

        qr.render(async (decodedText) => {
            const trackUri = decodedText.trim();
            await fetch(`https://api.spotify.com/v1/me/player`, {
                method: "PUT",
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    device_id: device_id,
                    uris: [trackUri]
                })
            });
        });
    });

    player.connect();
};
