
test:
	$(MAKE) clean
	$(MAKE) build
	lux *.lux


build:
	$(MAKE) -C packages/frobnicator/src
	$(MAKE) -C packages/apply-config-template/src
	$(MAKE) ncs-runtime


netsim:
	ncs-netsim create-network packages/frobnicator 2 frob


ncs-runtime: netsim ncs.conf
	rm -rf ./$@
	ncs-setup --dest ./$@ --package packages/apply-config-template
	cp ncs.conf ./$@


clean:
	$(MAKE) -k -C packages/frobnicator/src clean || true
	$(MAKE) -k -C packages/apply-config-template/src clean || true
	rm -rf netsim ncs-runtime
	rm -rf lux_logs


start:
	ncs-netsim start
	cd ncs-runtime && ncs

stop:
	ncs-netsim stop || true
	ncs --stop || true
