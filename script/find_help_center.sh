#!/bin/bash

ZIP="$1"

RESULT=$(mysql -u asterisk -ppasser safe_db -N -e "
SELECT CONCAT(
    'Le centre d''aide le plus proche de votre localité est ', hc.name,
    '. Vous pouvez les contacter au ', hc.phone, '. Merci pour votre appel, et prenez soin de vous.'
)
FROM help_centers hc
JOIN zipcode_coords zc_user ON zc_user.zipcode = '$ZIP'
ORDER BY SQRT(POW(hc.latitude - zc_user.latitude, 2) + POW(hc.longitude - zc_user.longitude, 2))
LIMIT 1;
")


echo "$RESULT" > /tmp/helpinfo.txt

# Génère le fichier audio initial
pico2wave -l fr-FR -w /tmp/helpinfo_raw.wav "$RESULT"

# Convertit en 8000Hz mono WAV lisible par Asterisk
sox /tmp/helpinfo_raw.wav -r 8000 -c 1 /tmp/helpinfo.wav tempo 0.75

# Optionnel : supprimer le fichier temporaire brut
rm /tmp/helpinfo_raw.wav

