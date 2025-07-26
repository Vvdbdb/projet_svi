#!/bin/bash

ZIP="$1"

RESULT=$(mysql -u asterisk -ppasser safe_db -N -e "
SELECT CONCAT(
    'The help center nearest to your location is ', hc.name,
    '. You can contact them at ', hc.phone, '. Thank you for your call, and take care.'
)
FROM help_centers hc
JOIN zipcode_coords zc_user ON zc_user.zipcode = '$ZIP'
ORDER BY SQRT(POW(hc.latitude - zc_user.latitude, 2) + POW(hc.longitude - zc_user.longitude, 2))
LIMIT 1;
")


echo "$RESULT" > /tmp/helpinfo.txt

# Génère le fichier audio initial
pico2wave -l en-GB -w /tmp/helpinfo_raw.wav "$RESULT"

# Convertit en 8000Hz mono WAV lisible par Asterisk
sox /tmp/helpinfo_raw.wav -r 8000 -c 1 /tmp/helpinfo.wav tempo 0.75

# Optionnel : supprimer le fichier temporaire brut
rm /tmp/helpinfo_raw.wav

