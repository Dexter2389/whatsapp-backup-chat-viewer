from src.models import Call, CallLog, Contact

expected_build_call_for_given_id_results = [
    Call(
        call_row_id=929,
        from_me=1,
        timestamp=1545829680246,
        video_call=0,
        duration=0,
        call_result=4,
    ),
    Call(
        call_row_id=2909,
        from_me=1,
        timestamp=1568973142212,
        video_call=0,
        duration=0,
        call_result=2,
    ),
    None,
]


expected_build_call_log_for_given_id_or_phone_number_results = [
    CallLog(
        jid_row_id=1,
        caller_id=Contact(
            raw_string_jid="728678956227@s.whatsapp.net",
            name="Jindra Otto",
            number="+728678956227",
        ),
        calls=[
            Call(
                call_row_id=590,
                from_me=1,
                timestamp=1542355690270,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=929,
                from_me=1,
                timestamp=1545829680246,
                video_call=0,
                duration=0,
                call_result=4,
            ),
            Call(
                call_row_id=1932,
                from_me=1,
                timestamp=1562486958110,
                video_call=0,
                duration=16,
                call_result=5,
            ),
            Call(
                call_row_id=2346,
                from_me=1,
                timestamp=1565016598310,
                video_call=0,
                duration=49,
                call_result=5,
            ),
        ],
    ),
    CallLog(
        jid_row_id=179,
        caller_id=Contact(
            raw_string_jid="576697466685@s.whatsapp.net",
            name="Hameed Teahan",
            number="+576697466685",
        ),
        calls=[],
    ),
    CallLog(
        jid_row_id=16,
        caller_id=Contact(
            raw_string_jid="669233817152@s.whatsapp.net",
            name="Izebel Bengtsdotter",
            number="+669233817152",
        ),
        calls=[
            Call(
                call_row_id=2909,
                from_me=1,
                timestamp=1568973142212,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=4001,
                from_me=1,
                timestamp=1578931156601,
                video_call=0,
                duration=5525,
                call_result=5,
            ),
        ],
    ),
]

expected_build_all_call_logs = [
    CallLog(
        jid_row_id=1,
        caller_id=Contact(
            raw_string_jid="728678956227@s.whatsapp.net",
            name="Jindra Otto",
            number="+728678956227",
        ),
        calls=[
            Call(
                call_row_id=590,
                from_me=1,
                timestamp=1542355690270,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=929,
                from_me=1,
                timestamp=1545829680246,
                video_call=0,
                duration=0,
                call_result=4,
            ),
            Call(
                call_row_id=1932,
                from_me=1,
                timestamp=1562486958110,
                video_call=0,
                duration=16,
                call_result=5,
            ),
            Call(
                call_row_id=2346,
                from_me=1,
                timestamp=1565016598310,
                video_call=0,
                duration=49,
                call_result=5,
            ),
        ],
    ),
    CallLog(
        jid_row_id=4,
        caller_id=Contact(
            raw_string_jid="491294924664@s.whatsapp.net",
            name="Faustina Papp",
            number="+491294924664",
        ),
        calls=[
            Call(
                call_row_id=4,
                from_me=1,
                timestamp=1538386901151,
                video_call=0,
                duration=12,
                call_result=5,
            ),
            Call(
                call_row_id=130,
                from_me=1,
                timestamp=1539341224536,
                video_call=0,
                duration=0,
                call_result=4,
            ),
            Call(
                call_row_id=467,
                from_me=1,
                timestamp=1541753228380,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=468,
                from_me=1,
                timestamp=1541753251499,
                video_call=0,
                duration=103,
                call_result=5,
            ),
        ],
    ),
    CallLog(
        jid_row_id=10,
        caller_id=Contact(
            raw_string_jid="988512899900@s.whatsapp.net",
            name="Hesiod Rautio",
            number="+988512899900",
        ),
        calls=[
            Call(
                call_row_id=2010,
                from_me=1,
                timestamp=1563071225820,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=2372,
                from_me=0,
                timestamp=1565278097000,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=3776,
                from_me=0,
                timestamp=1576251265000,
                video_call=0,
                duration=16,
                call_result=5,
            ),
            Call(
                call_row_id=4058,
                from_me=0,
                timestamp=1579849367000,
                video_call=0,
                duration=0,
                call_result=2,
            ),
        ],
    ),
    CallLog(
        jid_row_id=11,
        caller_id=Contact(
            raw_string_jid="635455887180@s.whatsapp.net",
            name="Josefína Šimunović",
            number="+635455887180",
        ),
        calls=[
            Call(
                call_row_id=2384,
                from_me=1,
                timestamp=1565348087633,
                video_call=0,
                duration=44,
                call_result=5,
            ),
            Call(
                call_row_id=2417,
                from_me=1,
                timestamp=1565775483975,
                video_call=0,
                duration=50,
                call_result=5,
            ),
            Call(
                call_row_id=4202,
                from_me=0,
                timestamp=1581099867000,
                video_call=0,
                duration=25,
                call_result=5,
            ),
            Call(
                call_row_id=9845,
                from_me=1,
                timestamp=1626916194248,
                video_call=0,
                duration=626,
                call_result=5,
            ),
        ],
    ),
    CallLog(
        jid_row_id=16,
        caller_id=Contact(
            raw_string_jid="669233817152@s.whatsapp.net",
            name="Izebel Bengtsdotter",
            number="+669233817152",
        ),
        calls=[
            Call(
                call_row_id=2909,
                from_me=1,
                timestamp=1568973142212,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=4001,
                from_me=1,
                timestamp=1578931156601,
                video_call=0,
                duration=5525,
                call_result=5,
            ),
        ],
    ),
    CallLog(
        jid_row_id=18,
        caller_id=Contact(
            raw_string_jid="589431685089@s.whatsapp.net",
            name="Oddbjørn Marques",
            number="+589431685089",
        ),
        calls=[
            Call(
                call_row_id=2699,
                from_me=1,
                timestamp=1567623957043,
                video_call=0,
                duration=74,
                call_result=5,
            ),
            Call(
                call_row_id=4119,
                from_me=1,
                timestamp=1580552346905,
                video_call=0,
                duration=0,
                call_result=2,
            ),
        ],
    ),
    CallLog(
        jid_row_id=32,
        caller_id=Contact(
            raw_string_jid="531551834307@s.whatsapp.net",
            name="Lennon Wortham",
            number="+531551834307",
        ),
        calls=[
            Call(
                call_row_id=8389,
                from_me=0,
                timestamp=1615381692000,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=10015,
                from_me=1,
                timestamp=1628793250207,
                video_call=0,
                duration=1168,
                call_result=5,
            ),
            Call(
                call_row_id=10176,
                from_me=1,
                timestamp=1630137988572,
                video_call=0,
                duration=1133,
                call_result=5,
            ),
        ],
    ),
    CallLog(
        jid_row_id=133,
        caller_id=Contact(
            raw_string_jid="922359962900@s.whatsapp.net",
            name="Mattheus Knepp",
            number="+922359962900",
        ),
        calls=[
            Call(
                call_row_id=1632,
                from_me=0,
                timestamp=1556731315000,
                video_call=0,
                duration=165,
                call_result=5,
            ),
            Call(
                call_row_id=2170,
                from_me=0,
                timestamp=1563691862000,
                video_call=0,
                duration=23,
                call_result=5,
            ),
            Call(
                call_row_id=3426,
                from_me=0,
                timestamp=1573708856000,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=8042,
                from_me=0,
                timestamp=1611287782000,
                video_call=1,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=9516,
                from_me=0,
                timestamp=1624379697000,
                video_call=1,
                duration=18,
                call_result=5,
            ),
            Call(
                call_row_id=9610,
                from_me=0,
                timestamp=1625390378000,
                video_call=0,
                duration=23,
                call_result=5,
            ),
            Call(
                call_row_id=10106,
                from_me=0,
                timestamp=1629685517000,
                video_call=1,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=10493,
                from_me=0,
                timestamp=1634728034000,
                video_call=0,
                duration=0,
                call_result=2,
            ),
        ],
    ),
    CallLog(
        jid_row_id=291,
        caller_id=Contact(
            raw_string_jid="997863428668@s.whatsapp.net",
            name="Sung-Soo Kyler",
            number="+997863428668",
        ),
        calls=[
            Call(
                call_row_id=2342,
                from_me=1,
                timestamp=1565016395279,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=2344,
                from_me=1,
                timestamp=1565016573402,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=2345,
                from_me=1,
                timestamp=1565016589402,
                video_call=0,
                duration=0,
                call_result=2,
            ),
            Call(
                call_row_id=2398,
                from_me=1,
                timestamp=1565511266208,
                video_call=0,
                duration=0,
                call_result=2,
            ),
        ],
    ),
]