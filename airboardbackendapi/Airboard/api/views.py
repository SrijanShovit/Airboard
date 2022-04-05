from rest_framework import viewsets, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

# Create your views here.
################################ USER VIEWSETS ###########################
# CREATE A NEW USER
class NewUser(APIView):
    def post(self, request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


################################ TEAM VIEWSETS ################################
# LIST OF TEAMS JOINED BY A USER TEACHER OR STUDENT
# CREATE UPDATE AND DELETE A TEAM BY A TEACHER
class TeamModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    serializer_class = TeamSerializer
    # GET TEAMS JOINED BY A USER
    def get_queryset(self):
        return set(Team.objects.filter(teacher=self.request.user) | 
                    Team.objects.filter(students=self.request.user))
    

    # CREATE A TEAM BY A TEACHER
    def create(self, request):
        if self.request.user.is_teacher:
            return super().create(request)
        else:
            return Response({"message": "not allowed to create team"}, status=status.HTTP_403_FORBIDDEN)
    

    # DELETE A TEAM CREATED BY SAME TEACHER
    def destroy(self, request, *args, **kwargs):
        team = Team.objects.get(pk=kwargs['pk'])
        if self.request.user.is_teacher and team.teacher == self.request.user:
            super().perform_destroy(team)
            return Response({"status":status.HTTP_204_NO_CONTENT})
        else:
            return Response({"message": "not allowed to delete team"}, status=status.HTTP_403_FORBIDDEN)
    

    # GET ALL SESSIONS OF A TEAM
    def retrieve(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
            if team.teacher != self.request.user and not team.students.filter(username=self.request.user).exists():
                return Response({"message": "You are not in this team"}, status=status.HTTP_403_FORBIDDEN)
            sessions = Session.objects.filter(team=team)
            team_serializer = TeamSerializer(team)
            session_serializer = SessionModelSerializer(sessions, many=True)
            return Response({"status": status.HTTP_200_OK, "team": team_serializer.data, "sessions": session_serializer.data})
        except:
            return Response({"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)



# TEACHER ADD AND REMOVE STUDENT IN CLASS
class AddRemoveStudent(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    # ADD STUDENT IN A TEAM
    def post(self, request):
        team_id = request.data.get('team_id')
        student_username = request.data.get('student_username')

        try: team = Team.objects.get(pk=team_id, teacher=self.request.user)
        except: return Response({"message": "Team not found or you don't have permission to add student"}, status=status.HTTP_404_NOT_FOUND)
        try: student = User.objects.get(username=student_username)
        except: return Response({"message": f"Username {student_username} not found"}, status=status.HTTP_404_NOT_FOUND)
        team.students.add(student)
        return Response({"message": f"Successfully added {student_username} to the team"}, status=status.HTTP_200_OK)
        
    
    # REMOVE STUDENT FROM TEAM
    def delete(self, request):
        team_id = request.data.get('team_id')
        student_username = request.data.get('student_username')

        try: team = Team.objects.get(pk=team_id, teacher=self.request.user)
        except: return Response({"message": "Team not found or you don't have permission to delete student"}, status=status.HTTP_404_NOT_FOUND)
        try: student = User.objects.get(username=student_username)
        except: return Response({"message": f"Username {student_username} not found"}, status=status.HTTP_404_NOT_FOUND)
        team.students.remove(student)
        return Response({"message": f"Successfully removed {student_username} from the team"}, status=status.HTTP_200_OK)



################################ SESSION VIEWSETS ################################
# GET A SINGLE SESSION DATA
class SessionAPI(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    # GET CURRENT SESSION DATA
    def get(self, request, session_id):
        try:
            session = Session.objects.get(pk=session_id)
            session_serializer = SingleSessionSerializer(session)

            team = session.team
            if team.teacher != self.request.user and not team.students.filter(username=self.request.user).exists():
                return Response({"message": "You are not in this team"}, status=status.HTTP_403_FORBIDDEN)
            
            return Response({"session": session_serializer.data})
        except Exception as e:
            print(e) 
            return Response({"message": "Session not found"}, status=status.HTTP_404_NOT_FOUND)



# CREATE DELETE AND UPDATE A SESSION
class CreateDeleteSession(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    # TODO CREATE A SESSION BY TEACHER
    def post(self, request):
        team_id = request.data.get('team_id')
        session_name = request.data.get('session_name')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        try: team = Team.objects.get(pk=team_id, teacher=self.request.user)
        except: return Response({"message": "Team not found or you don't have permission to add session"}, status=status.HTTP_404_NOT_FOUND)
        
        session = Session(team=team, session_name=session_name, start_time=start_time, end_time=end_time)
        session = SessionModelSerializer(session)
        if session.is_valid():
            session.save()
            return Response({"message": "Session created successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(session.errors, status=status.HTTP_404_NOT_FOUND)


    # UPDATE SESSION DATA and CHECK WHICH USER HAS THE PERMISSION
    def patch(self, request):
        pass


    # DELETE A SESSION BY TEACHER
    def delete(self, request):
        team_id = request.data.get('team_id')
        session_id = request.data.get('session_id')

        try: team = Team.objects.get(pk=team_id, teacher=self.request.user)
        except: return Response({"message": "Team not found or you don't have permission to delete student"}, status=status.HTTP_404_NOT_FOUND)
        try: session = Session.objects.get(session_id=session_id, team=team)
        except: return Response({"message": "Session not found"}, status=status.HTTP_204_NO_CONTENT)

        session.delete()
        return Response({"message": "Session deleted successfully"}, status=status.HTTP_200_OK)

