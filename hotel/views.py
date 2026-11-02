from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HotelManager(APIView):

    def post(self, request):

        data = request.data

        hotel = hotel.objects.create(
            name=data.get('name'),
            location=data.get('location'),
            phone=data.get('phone'),
            email=data.get('email'),
            description=data.get('description'),
            rating=data.get('rating')
        )

        return Response({
            'message': 'Hotel added successfully',
            'hotel_id': hotel.id
        }, status=status.HTTP_201_CREATED)

    def get(self, request):

        hotels = hotel.objects.all()

        data = []

        for hotel in hotels:
            data.append({
                'id': hotel.id,
                'name': hotel.name,
                'location': hotel.location,
                'phone': hotel.phone,
                'email': hotel.email,
                'description': hotel.description,
                'rating': hotel.rating
            })

        return Response(data)


class HotelDetails(APIView):

    def get(self, request, id):

        try:
            hotel = hotel.objects.get(id=id)

            data = {
                'id': hotel.id,
                'name': hotel.name,
                'location': hotel.location,
                'phone': hotel.phone,
                'email': hotel.email,
                'description': hotel.description,
                'rating': hotel.rating
            }

            return Response(data)

        except hotel.DoesNotExist:
            return Response(
                {'message': 'Hotel not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, id):

        try:
            hotel = hotel.objects.get(id=id)

            hotel.name = request.data.get('name', hotel.name)
            hotel.location = request.data.get('location', hotel.location)
            hotel.phone = request.data.get('phone', hotel.phone)
            hotel.email = request.data.get('email', hotel.email)
            hotel.description = request.data.get('description', hotel.description)
            hotel.rating = request.data.get('rating', hotel.rating)

            hotel.save()

            return Response({
                'message': 'Hotel updated successfully'
            })

        except hotel.DoesNotExist:
            return Response(
                {'message': 'Hotel not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, id):

        try:
            hotel = hotel.objects.get(id=id)

            hotel.delete()

            return Response({
                'message': 'Hotel deleted successfully'
            })

        except hotel.DoesNotExist:
            return Response(
                {'message': 'Hotel not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class RoomManager(APIView):

    def post(self, request):

        data = request.data

        try:
            hotel = hotel.objects.get(id=data.get('hotel_id'))

            room = room.objects.create(
                hotel=hotel,
                room_number=data.get('room_number'),
                room_type=data.get('room_type'),
                price=data.get('price'),
                capacity=data.get('capacity'),
                is_available=data.get('is_available', True)
            )

            return Response({
                'message': 'Room added successfully',
                'room_id': room.id
            }, status=status.HTTP_201_CREATED)

        except hotel.DoesNotExist:
            return Response(
                {'message': 'Hotel not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request):

        rooms = room.objects.all()

        data = []

        for room in rooms:
            data.append({
                'id': room.id,
                'hotel': room.hotel.name,
                'room_number': room.room_number,
                'room_type': room.room_type,
                'price': room.price,
                'capacity': room.capacity,
                'is_available': room.is_available
            })

        return Response(data)


class BookingManager(APIView):

    def post(self, request):

        data = request.data

        try:
            room = room.objects.get(id=data.get('room_id'))

            if not room.is_available:
                return Response(
                    {'message': 'Room is not available'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            booking = booking.objects.create(
                room=room,
                customer_name=data.get('customer_name'),
                customer_email=data.get('customer_email'),
                customer_phone=data.get('customer_phone'),
                check_in=data.get('check_in'),
                check_out=data.get('check_out'),
                guests=data.get('guests')
            )

            room.is_available = False
            room.save()

            return Response({
                'message': 'Room booked successfully',
                'booking_id': booking.id
            }, status=status.HTTP_201_CREATED)

        except room.DoesNotExist:
            return Response(
                {'message': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request):

        bookings = booking.objects.all()

        data = []

        for booking in bookings:
            data.append({
                'id': booking.id,
                'room': booking.room.room_number,
                'hotel': booking.room.hotel.name,
                'customer_name': booking.customer_name,
                'customer_email': booking.customer_email,
                'customer_phone': booking.customer_phone,
                'check_in': booking.check_in,
                'check_out': booking.check_out,
                'guests': booking.guests
            })

        return Response(data)