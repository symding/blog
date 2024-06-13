# /bin/bash
python3 collect_post.sh
cd ..
rm -rf ./build
npm run build
cp ./config/nginx.conf ./build/
cp ./AboutCareer/logo.svg ./build/
cd ./build;zip -r ../deploy/code.zip .;cd ../deploy;
python3 aliyun_fc_update.py 
rm -rf code.zip
rm -rf ../build
