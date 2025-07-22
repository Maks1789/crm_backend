from rest_framework import serializers
from .models import Event, Client
from django.contrib.auth import get_user_model

User = get_user_model()

# Серіалізатор для User (якщо потрібен для вкладених серіалізаторів)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] # Або інші потрібні поля


class EventSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(

        default=serializers.CurrentUserDefault()
    )

    # Додаткове поле для фронтенду (className для react-big-calendar)
    className = serializers.SerializerMethodField()
    client_name = serializers.CharField(source='client.__str__', read_only=True)
    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'clients',
            'client_name',
            'description',
            'start',
            'end',
            'event_type',
            'owner',
            'className',
            'created_at',
            'updated_at',
            'price',
            'payed',
            'performed',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_className(self, obj):
        # Відповідність між event_type і класами для CSS
        type_to_class = {
            'meeting': 'rbc-event-meeting',
            'presentation': 'rbc-event-presentation',
            'training': 'rbc-event-training',
            'dinner': 'rbc-event-dinner',
            'other': 'rbc-event-other'
        }
        return type_to_class.get(obj.event_type, 'rbc-event')

    def validate(self, data):
        """
        Перевірка, що дата початку передує даті завершення
        """
        if data['start'] > data['end']:
            raise serializers.ValidationError(
                "Дата завершення повинна бути після дати початку"
            )
        return data


class ClientSerializer(serializers.ModelSerializer):
    # ✅ Це поле тільки для ЧИТАННЯ. Воно повертає повні дані власника.
    # DRF НЕ намагатиметься валідувати його при POST/PUT, оскільки воно read_only.
    owner = UserSerializer(read_only=True)

    # ❌ ВИДАЛИТИ ЦЕ ПОЛЕ! Воно спричиняє помилку "Це поле обов'язкове."
    # owner_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), source='owner', write_only=True
    # )

    class Meta:
        model = Client
        fields = '__all__'  # Або перерахуйте конкретні поля, які ви хочете експонувати
        # ✅ 'owner' тепер не потрібно додавати до read_only_fields тут,
        # оскільки він вже визначений вище як read_only=True.
        read_only_fields = ['first_contact', 'last_contact', 'created_at', 'updated_at']

        # ✅ Цей метод тепер буде викликатися, оскільки валідація не буде провалюватися через owner_id

    def create(self, validated_data):
        # Якщо 'owner' не був наданий у validated_data (що буде завжди,
        # оскільки owner=UserSerializer(read_only=True)),
        # і якщо контекст запиту доступний, встановлюємо owner на поточного користувача.
        if 'owner' not in validated_data and self.context.get('request'):
            validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)