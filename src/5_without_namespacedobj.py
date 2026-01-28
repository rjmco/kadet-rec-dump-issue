"""A module which reproduce the Kadet's dump() issue without NamespacedObj class."""

from kadet import BaseObj


class Container(BaseObj):
    """Represents a Kubernetes Container."""

    def body(self):
        """Define a Kubernetes Deployment's manifest."""
        self.root.name = "a-container"
        self.root.image = "busybox"


class Deployment(BaseObj):
    """Represents a Kubernetes Deployment."""

    def new(self):
        """Return a new Deployment."""
        self.need("name")
        self.need("namespace")
        self.optional("containers")

        self.kwargs.apiVersion = "apps/v1"
        self.kwargs.kind = "Deployment"
        super().new()

    def body(self):
        """Define Deployment manifest."""
        self.root.apiVersion = self.kwargs.apiVersion
        self.root.kind = self.kwargs.kind
        self.root.metadata.name = self.kwargs.name
        self.root.metadata.namespace = self.kwargs.namespace
        if self.kwargs.containers:
            self.root.spec.template.spec.containers = self.kwargs.containers
        super().body()


def main():
    """Demonstrate Kadet recursive dump() issue."""
    main_obj = BaseObj()
    my_deploy = Deployment(name="my-deploy", namespace="my-space", containers=Container())
    main_obj.root.update(my_deploy.root)
    print(main_obj.dump())


if __name__ == "__main__":
    main()
