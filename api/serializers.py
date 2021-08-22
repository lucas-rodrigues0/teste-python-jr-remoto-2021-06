from rest_framework import serializers

from .models import PackageRelease, Project
from api.package_validation import package_validation


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

        packages = validated_data["packages"]
        for package in packages:
            package = package_validation(package)
            if "error" in package.keys():
                raise serializers.ValidationError(package, code=400)

        project = Project.objects.create(name=validated_data["name"])
        for package in packages:
            PackageRelease.objects.create(project=project, **package)
        return {
            "name": Project(name=validated_data["name"]),
            "packages": [*packages],
        }
