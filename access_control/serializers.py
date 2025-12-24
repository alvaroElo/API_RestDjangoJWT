from rest_framework import serializers
from .models import Usuario, Departamento, Sensor, Barrera, Evento


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'rol', 'telefono', 'is_active', 'password', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Usuario(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        return value


class SensorSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Sensor
        fields = '__all__'

    def validate_uid_mac(self, value):
        # Validar que el UID/MAC sea único
        if self.instance:  # Update
            if Sensor.objects.exclude(pk=self.instance.pk).filter(uid_mac=value).exists():
                raise serializers.ValidationError("Ya existe un sensor con este UID/MAC")
        else:  # Create
            if Sensor.objects.filter(uid_mac=value).exists():
                raise serializers.ValidationError("Ya existe un sensor con este UID/MAC")
        return value

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        return value


class BarreraSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = Barrera
        fields = '__all__'

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        return value


class EventoSerializer(serializers.ModelSerializer):
    sensor_nombre = serializers.CharField(source='sensor.nombre', read_only=True)
    barrera_nombre = serializers.CharField(source='barrera.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario_responsable.username', read_only=True)
    
    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ['timestamp']
