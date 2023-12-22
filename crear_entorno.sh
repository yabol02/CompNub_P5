#! /bin/bash

cd /home/alumno/P5
kubectl delete ns delicias-p5 ibiza-p5 madrid-p5
kubectl apply -f delicias-f1.yaml
kubectl apply -f delicias-f2.yaml
kubectl apply -f ibiza-f1.yaml
kubectl apply -f ibiza-f2.yaml
kubectl apply -f alertmanager.yaml
kubectl apply -f ingress-f3.yaml