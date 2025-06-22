import streamlit as st
from datetime import datetime, timedelta, time
from obj.event import Event
from obj.event_admins import EventAdmins
from utils import validation, db
from sqlalchemy.orm import sessionmaker, Session
import hashlib

def submit_event(event: Event):
    Session = sessionmaker(db.get_engine())
    with Session() as session:
        session.add(event)
        event_query = session.query(Event)
        event_id = event_query.filter(Event.event_name == event.event_name).first().id
        insert_event_admin(event_id, user_permission='owner', session=session)
        session.commit()
        st.success(f'Event {event.event_name} was created successfully', icon='✅')
        # st.toast(f'Event {event.event_name} was inserted successfully')

def lookup_event(event_name: str) -> Event:
    Session = sessionmaker(db.get_engine())
    with Session() as session:
        event_query = session.query(Event)
        returned_event = event_query.filter(Event.event_name==event_name).first()
        return returned_event

def update_karaoke_event(event: Event):
    print('in update event')
    Session = sessionmaker(db.get_engine())
    with Session() as session:
        event_query = session.query(Event)
        target_event = event_query.filter(Event.id==event.id)
        print('Found event', event.id)
        # print(target_event.id)
        target_event.update({
            Event.event_name: event.event_name,
            Event.event_date: event.event_date,
            Event.nomination_end_timestamp: event.nomination_end_timestamp,
            Event.voting_end_timestamp: event.voting_end_timestamp,
            Event.song_nomination_limit: event.song_nomination_limit,
            Event.song_delay: event.song_delay,
        })
        session.commit()
        return target_event.first()
        # event_query.update(event)
        # returned_event = event_query.filter(Event.event_name==event_name).first()
        # return returned_event
    # pass

def insert_event_admin(event_id: int, user_permission: str, session: Session):
    admin = EventAdmins(
        event_id = event_id,
        user_id = hashlib.sha256(st.user.email.encode()).hexdigest(),
        user_permission = user_permission
    )
    session.add(admin)
    st.success(f'Set {st.user.email} as event {user_permission}', icon='✅')



if not st.user.is_logged_in:
    st.wriate('You should login first')
    st.stop()

create_event_tab, update_event_tab = st.tabs(['Create Event', 'Update Event'])

with create_event_tab:
    st.markdown("# Create a karaoke event 🎤🎶")

    with st.form(
            key='create_event',
            clear_on_submit=False,
            enter_to_submit=False,
        ) as create_event:

        event_name = st.text_input('Event name', max_chars=255, key='event_name', value=f'test1 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        event_date = st.date_input('Event date', min_value=datetime.today(), key='event_date', format='YYYY-MM-DD')

        col1, col2 = st.columns(2)
        with col1:
            nomination_end_date = st.date_input('Nomination end date', min_value=datetime.today(), key='nomination_end_date', format='YYYY-MM-DD')
            voting_end_date = st.date_input('Voting end date', min_value=datetime.today(), key='voting_end_date', format='YYYY-MM-DD')
        with col2:
            nomination_end_time = st.time_input('Nomination end time', key='nomination_end_time', step=900)
            voting_end_time = st.time_input('Voting end time', key='voting_end_time', step=900)
        # lock_voter_domain = st.checkbox('Lock voter domain', value=False, key='lock_voter_domain')
        song_limit = st.number_input('Songs limit', min_value=0, value=5, help='The number of songs users are allowed to nominate & vote for')
        required_domain = st.text_input('Voter email domain', max_chars=255, help='Must be an email domain like @example.com')
        song_delay = st.number_input('Songs delay', min_value=0, max_value=120, value=5, help='The expected time in seconds between each song and the next')


        submitted = st.form_submit_button("Create event")
        if submitted:
            with st.spinner(f'Creating event {event_name}'):
            # st.write('Creating event with the following details:')
                submitted_event = Event(
                    event_name=event_name,
                    event_date=event_date,
                    nomination_end_timestamp=datetime.combine(nomination_end_date, nomination_end_time),
                    voting_end_timestamp=datetime.combine(voting_end_date, voting_end_time),
                    song_nomination_limit=song_limit,
                    required_domain=required_domain,
                    lock_voter_domain=validation.domain_validation(required_domain),
                    song_delay=time(second=song_delay),
                )
                submit_event(submitted_event)
            # spinner

with update_event_tab:
    st.markdown("# Lookup an event")
    st.session_state['event_name_lookup'] = st.text_input('Insert event name', max_chars=255, value=st.session_state.get('event_name_lookup'))
    lookup = st.button('Lookup event')
    if lookup or st.session_state['event_name_lookup']:
        event_details = lookup_event(st.session_state.get('event_name_lookup'))
        if not event_details:
            st.warning('Could not find event named "' + st.session_state['event_name_lookup'] +'"', icon='⚠️')
            st.stop()
        st.write('Retrieved event')
        st.write(event_details.__dict__)
    else:
        st.write("Lookup event")
        st.stop()
    # event_details = lookup_event(st.session_state.get('event_name_lookup', 'test1'))

    with st.form(
            key='update_event',
            clear_on_submit=False,
            enter_to_submit=False,
        ) as update_event:

        st.number_input('Event ID', value=event_details.id, disabled=True)
        event_name = st.text_input('Event name', max_chars=255, value=event_details.event_name)
        event_date = st.date_input('Event date', min_value=datetime.today(), format='YYYY-MM-DD', value=event_details.event_date)

        col1, col2 = st.columns(2)
        with col1:
            nomination_end_date = st.date_input('Nomination end date', min_value=datetime.today(), format='YYYY-MM-DD', value=event_details.nomination_end_timestamp.date())
            voting_end_date = st.date_input('Voting end date', min_value=datetime.today(), format='YYYY-MM-DD', value=event_details.voting_end_timestamp.date())
        with col2:
            nomination_end_time = st.time_input('Nomination end time', step=900, value=event_details.nomination_end_timestamp.time())
            voting_end_time = st.time_input('Voting end time', step=900, value=event_details.voting_end_timestamp.time())
        lock_voter_domain = st.checkbox('Lock voter domain', value=event_details.lock_voter_domain, disabled=True)
        song_limit = st.number_input('Songs limit', min_value=0, value=event_details.song_nomination_limit, help='The number of songs users are allowed to nominate & vote for')
        required_domain = st.text_input('Voter email domain', max_chars=255, help='Must be an email domain like @example.com', value=event_details.required_domain, disabled=True)
        delay_in_seconds = int(timedelta(minutes=event_details.song_delay.minute, seconds=event_details.song_delay.second).total_seconds())
        song_delay = st.number_input('Songs delay', min_value=0, max_value=120, value=int(delay_in_seconds), help='The expected time in seconds between each song and the next')

        print('Update form rendered')
        submite_update = st.form_submit_button("Update event")
        if submite_update:
            print('Clicked submit')
            with st.spinner(f'Updating event {event_name}'):
                print('Passed spinner')
                st.write('event update submitted!!')
                updated_event = update_karaoke_event(Event(
                    id=event_details.id,
                    event_name=event_name,
                    event_date=event_date,
                    nomination_end_timestamp=datetime.combine(nomination_end_date, nomination_end_time),
                    voting_end_timestamp=datetime.combine(voting_end_date, voting_end_time),
                    song_nomination_limit=song_limit,
                    required_domain=required_domain,
                    lock_voter_domain=validation.domain_validation(required_domain),
                    song_delay=time(second=song_delay),
                ))
                st.write(updated_event.__dict__)
            st.success(f'Event {updated_event.event_name} was updated successfully', icon='✅')
