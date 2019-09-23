
WAIT := 200s

create:
	-@kind create cluster --name test --wait $(WAIT)

env:
	@kind get kubeconfig-path --name test

delete:
	@kind delete cluster --name test

list:
	@kind get clusters

.PHONY: create env delete list