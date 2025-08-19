s.boot;
s.latency = nil;
//s.reboot;
//s.freeAll;
//jackd -R -d alsa -d hw:3 -p64
//midisnoop

s.doWhenBooted({

~bs = SoundFile.collectIntoBuffers("/home/dozsam13/dev/PdSynth/samples/emx-sample-pack-50tube/*");

MIDIClient.init;
MIDIIn.connect(0, MIDIClient.sources.detectIndex{|src| src.device.contains("USB")});


//MIDISyncClock.init;

~midiOutIndex = MIDIClient.destinations.detectIndex{|src| src.device.contains("USB")};
~midiOut = MIDIOut(~midiOutIndex, MIDIClient.destinations[~midiOutIndex].uid); // .latency_(Server.default.latency);

MIDISyncClock.init;

//MIDISyncClock.tempo;



(
(
SynthDef.new(\sampy, {
	var sig, env, envgen, sig2;

	sig = PlayBuf.ar(
		numChannels: 2,
		bufnum: \buf.kr(0),
		rate: BufRateScale.kr(\buf.kr(0)) * \rate.kr(1),  //44100/44100
		startPos: \start_pos.kr(50)
	);
	/*env = Env.new(
		levels: [0, 1, 1, 0], // levels
		times: [\attack.kr(0.01), \sustain.kr(1.0), \release.kr(0.1)],
		curve: 'lin'
	).kr(doneAction: 2);*/

	env = EnvGen.ar(
		Env.perc(attackTime: \attack.kr(0.01), releaseTime: \release.kr(0.1), level: 1.0, curve: -1.0),
		doneAction: 2
	);
	//sig = GlitchBPF..ar(in: sig, freq: 440.0, rq: 1.0, mul: 1.0, add: 0.0);
	//sig = CrossoverDistortion.ar(sig, amp: \distortion_amp.kr(0.5), smooth: \distortion_smooth.kr(0.5), mul: 1.0, add: 0);
	sig = RLPF.ar(in: sig, freq: \cutoff.kr(2200.0), rq: \resonance.kr(0.01), mul: 1.0, add: 0.0);
	sig = env*sig*\mute.kr(1);
	Out.ar(\out.kr(0), sig*\amp.kr(1));
	Out.ar(15, sig*\reverb_send.kr(0));
	Out.ar(16, sig*\delay_send.kr(0));
}).add;
);

(
t = TempoClock.new(200/60).permanent_(true);

~sendMidiClock = { |beat|
    ~midiOut.midiClock;
    t.schedAbs(beat + (1/24);, ~sendMidiClock);
};

t.schedAbs(t.beats.ceil, ~sendMidiClock);
);

(
~track_ids = [1, 2];
~paramDict = Dictionary();
~patterns = [];
~track_ids.do({
	arg track_id;

	~paramDict.put(("amp_" ++ track_id).asSymbol, 0.0);
	~paramDict.put(("bufnum_" ++ track_id).asSymbol, ~bs[14].bufnum);
	~paramDict.put(("rate_" ++ track_id).asSymbol, Pseq([1.0], 1));
	~paramDict.put(("mute_" ++ track_id).asSymbol, 1.0);
	~paramDict.put(("freq_" ++ track_id).asSymbol, Pseq([\, \, \, \], 1));
	//AMP
	~paramDict.put(("start_pos_" ++ track_id).asSymbol, 0.0);
	~paramDict.put(("attack_" ++ track_id).asSymbol, 0.001);
	~paramDict.put(("sustain_" ++ track_id).asSymbol, 1.0);
	~paramDict.put(("release_" ++ track_id).asSymbol, 0.5);
	//FILTER
	~paramDict.put(("cutoff_" ++ track_id).asSymbol, 2200.0);
	~paramDict.put(("resonance_" ++ track_id).asSymbol, 0.1);
	//EFFECT
	~paramDict.put(("distortion_amp_" ++ track_id).asSymbol, 0.0);
	~paramDict.put(("distortion_smooth_" ++ track_id).asSymbol, 0.0);
	~paramDict.put(("reverb_send_" ++ track_id).asSymbol, 0.0);
	~paramDict.put(("delay_send_" ++ track_id).asSymbol, 0.0);
});
);
(
~patterns = ~track_ids.collect{
	arg track_id;

	// Create OSC param bindings
	OSCdef(("amp_" ++ track_id).asSymbol, { |msg|
		//msg[1].postln;
		~paramDict[("amp_" ++ track_id).asSymbol] = msg[1];
	}, "/amp_" ++ track_id);

	OSCdef(("bufnum_" ++ track_id).asSymbol, { |msg|
		//msg[1].postln;
		~paramDict[("bufnum_" ++ track_id).asSymbol] = msg[1];
	}, "/bufnum_" ++ track_id);

	OSCdef(("rate_" ++ track_id).asSymbol, { |msg|
		//msg[1].postln;
		~paramDict[("rate_" ++ track_id).asSymbol] = Pseq([msg[1]], 1);
	}, "/rate_" ++ track_id);

	OSCdef(("start_pos_" ++ track_id).asSymbol, { |msg|
		msg[1].postln;
		~paramDict[("start_pos_" ++ track_id).asSymbol] = msg[1];
	}, "/start_pos_" ++ track_id);

	OSCdef(("attack_" ++ track_id).asSymbol, { |msg|
		~paramDict[("attack_" ++ track_id).asSymbol] = msg[1];
	}, "/attack_" ++ track_id);

	OSCdef(("sustain_" ++ track_id).asSymbol, { |msg|
		~paramDict[("sustain_" ++ track_id).asSymbol] = msg[1];
	}, "/sustain_" ++ track_id);

	OSCdef(("release_" ++ track_id).asSymbol, { |msg|
		~paramDict[("release_" ++ track_id).asSymbol] = msg[1];
	}, "/release_" ++ track_id);

	OSCdef(("cutoff_" ++ track_id).asSymbol, { |msg|
		~paramDict[("cutoff_" ++ track_id).asSymbol] = msg[1];
	}, "/cutoff_" ++ track_id);

	OSCdef(("resonance_" ++ track_id).asSymbol, { |msg|
		~paramDict[("resonance_" ++ track_id).asSymbol] = msg[1];
	}, "/resonance_" ++ track_id);

	OSCdef(("distortion_smooth_" ++ track_id).asSymbol, { |msg|
		~paramDict[("distortion_smooth_" ++ track_id).asSymbol] = msg[1];
	}, "/distortion_smooth_" ++ track_id);

	OSCdef(("distortion_amp_" ++ track_id).asSymbol, { |msg|
		~paramDict[("distortion_amp_" ++ track_id).asSymbol] = msg[1];
	}, "/distortion_amp_" ++ track_id);

	OSCdef(("reverb_send_" ++ track_id).asSymbol, { |msg|
		msg[1].postln;
		~paramDict[("reverb_send_" ++ track_id).asSymbol] = msg[1];
	}, "/reverb_send_" ++ track_id);

	OSCdef(("delay_send_" ++ track_id).asSymbol, { |msg|
		msg[1].postln;
		~paramDict[("delay_send_" ++ track_id).asSymbol] = msg[1];
	}, "/delay_send_" ++ track_id);

	OSCdef(("mute_" ++ track_id).asSymbol, { |msg|
		~paramDict[("mute_" ++ track_id).asSymbol] = msg[1];
	}, "/mute_" ++ track_id);

	OSCdef(("freq_" ++ track_id).asSymbol, { |msg|
		var seq, s2;
		seq = msg.drop(1);
		seq.postln;
		~paramDict[("freq_" ++ track_id).asSymbol] = Pseq(seq, 1);
	}, "/freq_" ++ track_id);

	// Create Pattern for track
	Pbind(
		\instrument, \sampy,
		\dur, 0.25,
		\amp, Pfunc({~paramDict[("amp_" ++ track_id).asSymbol]}),
		\buf, Pfunc({~paramDict[("bufnum_" ++ track_id).asSymbol]}),
		\rate, Pn(Plazy({~paramDict[("rate_" ++ track_id).asSymbol]}), inf),
		\mute, Pfunc({~paramDict[("mute_" ++ track_id).asSymbol]}),
		\freq, Pn(Plazy({~paramDict[("freq_" ++ track_id).asSymbol]}), inf),
		//amp
		\start_pos, Pfunc({~paramDict[("start_pos_" ++ track_id).asSymbol]}),
		\attack, Pfunc({~paramDict[("attack_" ++ track_id).asSymbol]}),
		\sustain_, Pfunc({~paramDict[("sustain_" ++ track_id).asSymbol]}),
		\release, Pfunc({~paramDict[("release_" ++ track_id).asSymbol]}),
		//filter
		\cutoff, Pfunc({~paramDict[("cutoff_" ++ track_id).asSymbol]}),
		\resonance, Pfunc({~paramDict[("resonance_" ++ track_id).asSymbol]}),
		//effect
		\distortion_amp, Pfunc({~paramDict[("distortion_amp_" ++ track_id).asSymbol]}),
		\distortion_smooth, Pfunc({~paramDict[("distortion_smooth_" ++ track_id).asSymbol]}),
		\reverb_send, Pfunc({~paramDict[("reverb_send_" ++ track_id).asSymbol]}),
		\delay_send, Pfunc({~paramDict[("delay_send_" ++ track_id).asSymbol]})
	);
});

(
OSCdef(\start_seq, { |msg|
	"starting sequencer".postln;
	~players = ~patterns.collect({ |ptn|
		ptn.play(t)
		//ptn.play(MIDISyncClock)
	});
	~midiOut.start;
}, "/start_seq");

OSCdef(\stop_seq, { |msg|
	"stopping sequencer".postln;
	~players.do({ |player|
		player.stop;
	});
	~midiOut.stop;
}, "/stop_seq");

~startFunc = MIDIFunc.start({ |val|
    "MIDI START received".postln;
    ~players = ~patterns.collect({ |ptn|
		ptn.play(t)
		//ptn.play(MIDISyncClock)
	});
});

~stopFunc = MIDIFunc.stop({ |val|
    "MIDI STOP received".postln;
    ~players.do({ |player|
		player.stop;
	});
});
OSCdef(\bpm, { |msg|
	t.tempo = msg[1]/60;
}, "/bpm");

OSCdef(\volume, { |msg|
	s.volume.volume = if(msg[1] > 1) {1} {msg[1]};
}, "/volume");
);

//---------------------------------------------EFFECTS----------------------------------------------------
//REVERB
(
(
	{
		var sig;
		sig = In.ar(15, 1);
		sig = FreeVerb.ar(sig, mix: 0.9, room: 1.8, damp: 1.5);
		Out.ar(\out.kr(0),sig);
	}.play;
);
//DELAY
(
	{
		var sig;
		sig = In.ar(16, 1);
		sig = CombN.ar(sig,
			1.0, // max delay time
			0.25, // actual delay time (1/4 second)
			1.0 // decay time (feedback amount)
		);
	Out.ar(\out.kr(0), sig);
	}.play;
);
);

)



})

/*
~players = ~patterns.collect({ |ptn| ptn.play(t)});

~players.do({ |player| player.stop;});

~paramDict[("amp_1").asSymbol] = 1;
~paramDict[("amp_2").asSymbol] = 0;

~paramDict[("bufnum_1").asSymbol] = 1;
~paramDict[("attack_1").asSymbol] = 0.05;
~paramDict[("bufnum_2").asSymbol] = msg[1];

~paramDict[("attack_1").asSymbol] = 0.0;
~paramDict[("sustain_1").asSymbol] = 1.5;
~paramDict[("release_1").asSymbol] = 1.0;
s.freeAll;
s.queryAllNodes;
*/