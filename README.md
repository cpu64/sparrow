Build with: docker build -t cpu64/sparrow .

Run with: docker run --name sparrow -it --rm -v ./app:/app -v ./db:/db -p 5432:5432 -p 5000:5000 cpu64/sparrow
