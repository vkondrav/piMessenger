DATE=$(date +"%Y%m%d%H%M")
FILE=/mnt/large-storage/temp$DATE.temp
touch $FILE
echo "keep drive alive" $DATE > $FILE
rm $FILE
