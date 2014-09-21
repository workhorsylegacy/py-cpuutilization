
VERSION = 0.1.0

all:
	@echo build: Builds the python source dist package
	@echo install: Installs python source dist package
	@echo clean: Removes any generated files
	@echo rst: uses pandoc to generate the README.rst file from README.md

clean:
	rm -f -rf py_cpuutilization.egg-info
	rm -f -rf dist
	rm -f -rf py-cpuutilization-$(VERSION)
	rm -f -rf py-cpuutilization-$(VERSION).tar.gz

build: clean
	python setup.py sdist
	mv dist/py-cpuutilization-$(VERSION).tar.gz py-cpuutilization-$(VERSION).tar.gz
	rm -f -rf py_cpuutilization.egg-info
	rm -f -rf dist

install: remove
	tar xzf py-cpuutilization-$(VERSION).tar.gz
	cd py-cpuutilization-$(VERSION)/ && sudo python setup.py install
	rm -f -rf py-cpuutilization-$(VERSION)

	@echo now try "from cpuutilization import cpuutilization"
	@echo "cpuutilization.get_cpu_info()"

remove:
	sudo rm -f -rf /usr/local/lib/python2.7/dist-packages/py_cpuutilization-$(VERSION)-py2.7.egg

rst:
	rm -f -rf README.rst
	pandoc --from=markdown --to=rst --output=README.rst README.md



