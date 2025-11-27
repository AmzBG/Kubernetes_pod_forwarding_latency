for img in $(docker images --format "{{.Repository}}:{{.Tag}}" | grep '^pod'); do 
	echo "loading $img into minikube"
	minikube image load "$img"
done
