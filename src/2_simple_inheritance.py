"""A module which reproduce the Kadet's dump() issue with simple inheritance classes."""

from kadet import BaseObj


class Container(BaseObj):
    """Represents a Kubernetes Container."""

    def body(self):
        """Define a Kubernetes Deployment's manifest."""
        self.root.name = "a-container"
        self.root.image = "busybox"


class NamespacedObj(BaseObj):
    """Represents a Kubernetes namespaced object's manifest parts."""

    def new(self):
        """Return a new NamespacedObj."""
        self.need("name")
        self.need("namespace")
        self.need("apiVersion")
        self.need("kind")

    def body(self):
        """Define NamespacedObj manifest parts."""
        self.root.apiVersion = self.kwargs.apiVersion
        self.root.kind = self.kwargs.kind
        self.root.metadata.name = self.kwargs.name
        self.root.metadata.namespace = self.kwargs.namespace


class Deployment(NamespacedObj):
    """Represents a Kubernetes Deployment."""

    def new(self):
        """Return a new Deployment."""
        self.optional("containers")

        self.kwargs.apiVersion = "apps/v1"
        self.kwargs.kind = "Deployment"
        super().new()

    def body(self):
        """Define Deployment manifest."""
        if self.kwargs.containers:
            self.set_containers(self.kwargs.containers)
        super().body()

    def set_containers(self, containers):
        """Set the containers list on the spec template."""
        self.root.spec.template.spec.containers = containers


class MyDeployment(Deployment):
    """Represents MyDeployment's Kubernetes Deployment."""

    def new(self):
        """Return a new MyDeployment."""
        self.kwargs.containers = [Container()]
        super().new()


def main():
    """Demonstrate Kadet recursive dump() issue."""
    main_obj = BaseObj()
    my_deploy = MyDeployment(name="my-deploy", namespace="my-space")
    main_obj.root.update(my_deploy.root)
    print(main_obj.dump())


if __name__ == "__main__":
    main()
