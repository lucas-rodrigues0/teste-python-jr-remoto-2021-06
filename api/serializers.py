from rest_framework import serializers

from .models import PackageRelease, Project
from api.package_validation import package_versions


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        # TODO
        # - Processar os pacotes recebidos
        # - Persistir informações no banco
        packages = validated_data["packages"]
        for package in packages:
            versions = package_versions(package["name"])
            if versions == "error":
                return {"error": "One or more packages don't exist"}
            if (
                "version" in package.keys()
                and package["version"] not in versions
            ):
                return {"error": "One or more packages don't exist"}
            if "version" not in package.keys():
                package["version"] = list(versions)[-1]

        return Project(name=validated_data["name"])
