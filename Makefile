
WAIT := 200s
APPLY = kubectl apply --kubeconfig=$$(kind get kubeconfig-path --name test) --filename

create:
	-@kind create cluster --config deployments/kind/cluster.yaml --name test --wait $(WAIT)

env:
	@kind get kubeconfig-path --name test

delete:
	@kind delete cluster --name test

list:
	@kind get clusters

olm:
	@$(APPLY) https://github.com/operator-framework/operator-lifecycle-manager/releases/download/0.9.0/olm.yaml

postgres-operator:
	@$(APPLY) https://operatorhub.io/install/postgres-operator.yaml

app:
	@$(APPLY) deployments/fraud-detection

.PHONY: create env delete list