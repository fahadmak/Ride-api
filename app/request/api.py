from flask import jsonify, make_response, request
from flask.views import MethodView
from app.auth.decoractor import token_required
from app.models import Request, Ride


class RequestAPI(MethodView):
    """This class-based view for requesting a ride."""
    decorators = [token_required]

    def post(self, current_user, ride_id):
        if ride_id:
            try:
                request = Request(ride_id=ride_id)
                passenger = current_user[2]
                all_reqs = request.find_by_id(ride_id)
                for req in all_reqs:
                    req = {"Id": req['Id'], "ride_id": req['ride_id'],
                           "status": req['status'],
                           "passenger": req['passenger']}
                    if req in all_reqs:
                        return jsonify({'msg': 'You already requested\
                         to join this ride'}), 409

                request.insert(ride_id, passenger)
                return jsonify({'msg': 'A request to join this ride\
                 has been sent'}), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500

    def get(self, current_user, ride_id):
        '''Gets all requests'''
        try:
            request = Request(ride_id=ride_id)
            requests = request.find_by_id(ride_id)
            if requests == []:
                return jsonify({"msg": "You haven't recieved any ride\
                 requests yet"}), 200
            return jsonify(requests), 200
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    def put(self, current_user, ride_id, request_id):
        """Accept or reject a ride request"""
        # first check if the ride was created by the logged in driver
        ride = Ride(id=ride_id)
        the_ride = ride.find_by_id(ride_id)
        print(the_ride["driver"])
        print(current_user[2])
        if the_ride['driver'] == current_user[2]:
            data = request.get_json()
            if data['status'] == 'accepted' or data['status'] == 'rejected':
                try:
                    req = Request(id=request_id, ride_id=ride_id)
                    req.update_request(request_id, data)
                    response = {
                        'message': 'you have {} this ride request'
                        .format(data['status'])
                    }
                    return make_response(jsonify(response)), 200
                except Exception as e:
                    response = {
                        'message': str(e)
                    }
                    return make_response(jsonify(response)), 500
            response = {
                'message': 'The status can only be in 3 states,\
                requested, accepted and rejected'
            }
            return make_response(jsonify(response)), 406
        response = {
            'message': 'Forbidden access! You can only repond \
            to rides you created'
        }
        return jsonify(response)
