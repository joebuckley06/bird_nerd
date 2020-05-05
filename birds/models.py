# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.gis.db import models as gis_models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GeoStates(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=100)
    wikipedia = models.CharField(max_length=200)
    states = models.CharField(max_length=100)
    state_abbrev = models.CharField(max_length=100)
    geo = gis_models.MultiPolygonField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'geo_states'


class Layer(models.Model):
    topology = models.OneToOneField('Topology', models.DO_NOTHING, primary_key=True)
    layer_id = models.IntegerField()
    schema_name = models.CharField(max_length=10)
    table_name = models.CharField(max_length=10)
    feature_column = models.CharField(max_length=10)
    feature_type = models.IntegerField()
    level = models.IntegerField()
    child_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'layer'
        unique_together = (('topology', 'layer_id'), ('schema_name', 'table_name', 'feature_column'),)


class Routes(models.Model):
    id = models.IntegerField(primary_key=True)
    countrynum = models.IntegerField()
    statenum = models.IntegerField()
    route = models.IntegerField()
    routename = models.CharField(max_length=100)
    active = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    stratum = models.IntegerField()
    bcr = models.IntegerField()
    routetypeid = models.IntegerField()
    routetypedetailid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'routes'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class Species(models.Model):
    id = models.AutoField(primary_key=True)
    aou = models.IntegerField()
    english_common_name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'species'


class StateCodes(models.Model):
    countrynum = models.IntegerField()
    statenum = models.IntegerField()
    state_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'state_codes'


class Topology(models.Model):
    name = models.CharField(unique=True, max_length=10)
    srid = models.IntegerField()
    precision = models.FloatField()
    hasz = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'topology'


class UsStates(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    routedataid = models.IntegerField()
    countrynum = models.IntegerField()
    statenum = models.IntegerField()
    route = models.IntegerField()
    rpid = models.IntegerField()
    year = models.IntegerField()
    aou = models.IntegerField()
    count10 = models.IntegerField()
    count20 = models.IntegerField()
    count30 = models.IntegerField()
    count40 = models.IntegerField()
    count50 = models.IntegerField()
    stoptotal = models.IntegerField()
    speciestotal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'us_states'


class Weather(models.Model):
    id = models.IntegerField(primary_key=True)
    routedataid = models.IntegerField()
    countrynum = models.IntegerField()
    statenum = models.IntegerField()
    route = models.IntegerField()
    rpid = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    obsn = models.IntegerField()
    totalspp = models.IntegerField()
    starttemp = models.FloatField(blank=True, null=True)
    endtemp = models.FloatField(blank=True, null=True)
    tempscale = models.CharField(max_length=10)
    startwind = models.IntegerField()
    endwind = models.IntegerField()
    startsky = models.IntegerField()
    endsky = models.IntegerField()
    assistant = models.FloatField(blank=True, null=True)
    qualitycurrentid = models.IntegerField()
    runtype = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'weather'
