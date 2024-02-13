import base64
from django.contrib.auth.models import AnonymousUser
import requests
from django.core.files.base import ContentFile
from rest_framework import views, permissions
from rest_framework.response import Response
from .models import CarImage
from car.models import Car
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class ImageProcessView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근할 수 있도록 설정
    # permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        # base64로 인코딩된 이미지를 받음
        encoded_image = request.data.get('image')
        decoded_image = base64.b64decode(encoded_image)

        # 이미지를 임시 파일로 저장
        image_file = ContentFile(decoded_image, name='original_image.jpg')

        # 이미지 파일을 받음
        #image_file = request.FILES.get('image')

        # 이미지 객체 생성
        # if isinstance(request.user, AnonymousUser):
        #     car_image = CarImage.objects.create(original_image=image_file)
        # else:
        #     car_image = CarImage.objects.create(user=request.user, original_image=image_file)

        # 이미지 객체 생성
        car_image = CarImage.objects.create(user=request.user, original_image=image_file)

        # Flask 서버로 이미지 전송하고 결과 받기
        files = {'image': car_image.original_image.open()}
        response = requests.post('http://localhost:5000/process-image', files=files)
        result = response.json()
        #print(result)

        # vehicle_type이 이미 리스트 형태인 경우
        vehicle_type_list = result['vehicle_type']

        # 리스트에서 첫 번째 요소 사용하여 Car 모델 검색
        # 이 예에서는 리스트에 하나의 요소만 있다고 가정
        if vehicle_type_list:  # 리스트가 비어있지 않은 경우
            try:
                matching_car = Car.objects.get(name=vehicle_type_list[0])
                car_image.car = matching_car  # CarImage 모델에 참조 설정
            except Car.DoesNotExist:
                matching_car = None

        # base64로 인코딩된 이미지 데이터를 디코드
        car_image_data = base64.b64decode(result['car_image'])

        plate_image_data = base64.b64decode(result['plate_image'])
        enlarged_plate_image_data = base64.b64decode(result['enlarged_plate_images'])  # 예시로 첫 번째 이미지만 사용

        # 이미지 데이터를 ContentFile 객체로 변환
        car_image_file = ContentFile(car_image_data, name='car_image.png')
        plate_image_file = ContentFile(plate_image_data, name='plate_image.png')
        enlarged_plate_image_file = ContentFile(enlarged_plate_image_data, name='enlarged_plate_image.png')

        # 모델에 이미지 파일을 저장
        car_image.first_model_image.save('first_model_image.png', car_image_file, save=False)
        car_image.second_model_image.save('second_model_image.png', plate_image_file, save=False)
        car_image.license_plate_image.save('license_plate_image.png', enlarged_plate_image_file, save=False)
        # 차량 분류 결과
        car_image.vehicle_type = result['vehicle_type']
        # 번호판 OCR 결과
        car_image.license_plate_text = result['ocr_text']
        car_image.license_plate_vehicle_type = result['ocr_vehicle_type']
        # gpt 결과
        car_image.g_print = result['g_print']
        car_image.save()

        # 결과를 프론트엔드로 전송
        user = request.user

        response_data = {
            'id': car_image.id,
            'original_image_url': car_image.original_image.url,
            'first_model_image_url': car_image.first_model_image.url,
            'second_model_image_url': car_image.second_model_image.url,
            'license_plate_image_url': car_image.license_plate_image.url,
            'vehicle_type': car_image.vehicle_type,
            'license_plate_text': car_image.license_plate_text,
            'LICENSE_PLATE_VEHICLE_TYPE': car_image.license_plate_vehicle_type,
            'user_id': user.id,
            'g_print': car_image.g_print,
        }
        if matching_car:
            response_data.update({
                'car_id': matching_car.id,
                'displacement': matching_car.displacement,
                'name': matching_car.name,
                'carbon_tax': matching_car.carbon_tax,
                'carbon_emission': matching_car.carbon_emission,
                'class_label': matching_car.class_label
            })
        return Response(response_data)

    def get(self, request, *args, **kwargs):
        # 로그인한 사용자의 모든 이미지 처리 결과를 반환
        user = request.user
        car_images = CarImage.objects.filter(user=user).order_by('-id')  # 최신 순으로 정렬
        response_data_list = []

        for car_image in car_images:
            # 관련 Car 객체를 조회 (car_image.car 가 이미지에 연결된 Car 객체를 참조한다고 가정)
            try:
                car = car_image.car
                car_data = {
                    'displacement': car.displacement,
                    'name': car.name,
                    'carbon_tax': car.carbon_tax,
                    'carbon_emission': car.carbon_emission,
                    'class_label': car.class_label
                }
            except AttributeError:
                car_data = {}

            response_data = {
                "user_id": user.id,
                "username": user.username,
                "vehicle_type": car_image.vehicle_type,
                "license_plate_text": car_image.license_plate_text,
                "original_image_url": car_image.original_image.url,
                "first_model_image_url": car_image.first_model_image.url,
                "second_model_image_url": car_image.second_model_image.url,
                "license_plate_image_url": car_image.license_plate_image.url,
                'LICENSE_PLATE_VEHICLE_TYPE': car_image.license_plate_vehicle_type,
                "g_print": car_image.g_print,
            }

            response_data.update(car_data)
            response_data_list.append(response_data)

        return Response(response_data_list)
