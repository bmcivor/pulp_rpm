import gzip

from pulp.server.webservices.views import serializers as platform_serializers


class Distribution(platform_serializers.ModelSerializer):
    """
    Serializer for Distribution based models
    """
    class Meta:
        remapped_fields = {'distribution_id': 'id'}


class Drpm(platform_serializers.ModelSerializer):
    """
    Serializer for Drpm based models
    """
    class Meta:
        remapped_fields = {}


class RpmBase(platform_serializers.ModelSerializer):
    """
    Serializer for RpmBase based models
    """
    class Meta:
        remapped_fields = {}

    def serialize(self, unit):
        """
        Convert a single unit to it's dictionary form.

        Decompress values of the `repodata` dict field for RPM/SRPM units.

        :param unit: The object to be converted
        :type unit: object
        """
        for metadata_type in unit.get('repodata', {}):
            metadata = unit['repodata'][metadata_type]
            unit['repodata'][metadata_type] = gzip.zlib.decompress(metadata)
        return super(RpmBase, self).serialize(unit)


class Errata(platform_serializers.ModelSerializer):
    """
    Serializer for Errata models
    """
    class Meta:
        remapped_fields = {'errata_from': 'from',
                           'errata_id': 'id'}

    def serialize(self, unit):
        """
        Convert a single unit to it's dictionary form.

        Add to errratum unit its pkglist if needed.
        Duplicated pkglists are eliminated.

        :param unit: The object to be converted
        :type unit: object
        """
        from pulp_rpm.plugins.db import models

        # If pkglist field is absent, it's on purpose, e.g. not specified in the fields during
        # search. So it should not be added during serialization.
        # If pkglist field is present, it's always emtpy => it should be filled in.
        if 'pkglist' in unit:
            errata_id = unit.get('errata_id')

            # If fields in search criteria don't include errata_id
            if errata_id is None:
                erratum_obj = models.Errata.objects.only('errata_id').get(id=unit.get('_id'))
                errata_id = erratum_obj.errata_id

            pkglists = models.Errata.get_unique_pkglists(errata_id)
            coll_num = 0
            for pkglist in pkglists:
                for coll in pkglist:
                    # To preserve the original format of a pkglist the 'short' and 'name'
                    # keys are added. 'short' can be an empty string, collection 'name'
                    # should be unique within an erratum.
                    unit['pkglist'].append({'packages': coll,
                                            'short': '',
                                            'name': 'collection-%s' % coll_num})
                    coll_num += 1

        return super(Errata, self).serialize(unit)


class PackageGroup(platform_serializers.ModelSerializer):
    """
    Serializer for a PackageGroup models
    """
    class Meta:
        remapped_fields = {'package_group_id': 'id'}


class PackageCategory(platform_serializers.ModelSerializer):
    """
    Serializer for a PackageCategory models
    """
    class Meta:
        remapped_fields = {'package_category_id': 'id'}


class PackageEnvironment(platform_serializers.ModelSerializer):
    """
    Serializer for a PackageEnvironment models
    """
    class Meta:
        remapped_fields = {'package_environment_id': 'id'}


class PackageLangpacks(platform_serializers.ModelSerializer):
    """
    Serializer for a PackageLangpacks models
    """
    class Meta:
        remapped_fields = {}


class YumMetadataFile(platform_serializers.ModelSerializer):
    """
    Serializer for a YumMetadataFile models
    """
    class Meta:
        remapped_fields = {}


class ISO(platform_serializers.ModelSerializer):
    """
    Serializer for a ISO models
    """
    class Meta:
        remapped_fields = {}
