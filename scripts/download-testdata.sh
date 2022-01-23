#!/bin/sh

cd ..

mkdir -p ./coins/data/record_DE-MUS-062622_kenom_127703
wget -O ./coins/data/record_DE-MUS-062622_kenom_127703/vs.jpg https://sammlungen.uni-goettingen.de/api/v1/records/record_DE-MUS-062622_kenom_127703/files/images/record_DE-MUS-062622_kenom_127703_vs.jpg/full/full/0/default.jpg
wget -O ./coins/data/record_DE-MUS-062622_kenom_127703/rs.jpg https://sammlungen.uni-goettingen.de/api/v1/records/record_DE-MUS-062622_kenom_127703/files/images/record_DE-MUS-062622_kenom_127703_rs.jpg/full/full/0/default.jpg
wget -O ./coins/data/record_DE-MUS-062622_kenom_127703/manifest.json https://sammlungen.uni-goettingen.de/api/v1/records/record_DE-MUS-062622_kenom_127703/manifest
wget -O ./coins/data/record_DE-MUS-062622_kenom_127703/lido.xml $(jq -r '.seeAlso | select(.format == "text/xml")| .["@id"]' ./coins/data/record_DE-MUS-062622_kenom_127703/manifest.json)

mkdir -p ./desk/data/DE-611-HS-3461927


wget -O ./desk/data/DE-611-HS-3461927/00000001.jpg https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3461927:00000001/full/full/0/default.jpg
wget -O ./desk/data/DE-611-HS-3461927/00000002.jpg https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3461927:00000002/full/full/0/default.jpg
wget -O ./desk/data/DE-611-HS-3461927/00000003.jpg https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3461927:00000003/full/full/0/default.jpg
wget -O ./desk/data/DE-611-HS-3461927/00000004.jpg https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3461927:00000004/full/full/0/default.jpg
wget -O ./desk/data/DE-611-HS-3461927/00000005.jpg https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3461927:00000005/full/full/0/default.jpg
wget -O ./desk/data/DE-611-HS-3461927/00000006.jpg https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3461927:00000006/full/full/0/default.jpg
wget -O ./desk/data/DE-611-HS-3461927/00000007.jpg https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3461927:00000007/full/full/0/default.jpg
