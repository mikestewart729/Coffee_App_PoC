/// Utility function to get the current geolocation of the user, if possible
export const getCurrentPosition = () => {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation is not supported by your browser'))
            return
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                })
            },
            (error) => {
                let message = 'Unable to get location'
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        message = 'Location permission denied'
                        break
                    case error.POSITION_UNAVAILABLE:
                        message = 'Location information unavailable'
                        break
                    case error.TIMEOUT:
                        message = 'Location request timed out'
                        break
                }
                reject(new Error(message))
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0,
            }
        )
    })
}