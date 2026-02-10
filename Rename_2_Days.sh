
mkdir -p courses/dcs109 courses/dcs211
echo "Late work accepted up to 3 days." > courses/dcs109/syllabus.txt
echo "Late work accepted up to 3 days." > courses/dcs211/syllabus.txt

sed -i.bak 's/3 days/2 days/g' courses/*/syllabus.txt