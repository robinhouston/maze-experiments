#include <sysexits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <gmp.h>


/**
 * Compute the nth Fibonacci number with arbitrary-precision
 * floating-point arithmetic, using the formula fib(n) ≈ phi ^ n / sqrt(5)
 * (which is exact if you round the rhs to the nearest whole number).
 */
void fib_float(mpf_t *result, long n)
{
	mpf_t sqrt5, phi;
	mp_bitcnt_t bitcnt;

    /* We need about n lg(phi) bits of precision */
	bitcnt = n * 7 / 10;

	/* Initialise sqrt5 to the square root of 5 */
	mpf_init2(sqrt5, bitcnt);
	mpf_sqrt_ui(sqrt5, 5);

    /* Initialise phi to the Golden Ratio */
	mpf_init2(phi, bitcnt);
	mpf_set(phi, sqrt5);
	mpf_add_ui(phi, phi, 1);
	mpf_div_2exp(phi, phi, 1);

    /* Compute phi ^ n / sqrt5 */
	mpf_init2(*result, bitcnt);
	mpf_pow_ui(*result, phi, n);
	mpf_div(*result, *result, sqrt5);

	/* Dispose of the temporary variables */
	mpf_clear(sqrt5);
	mpf_clear(phi);
}

/**
 * Compute the nth Fibonacci number using both the floating-point
 * method and the integer algorithm, and print the relative timings.
 *
 * Also check both methods give the same result, just to be sure.
 *
 * (As expected, this shows that the integer method is much faster.)
 */
int main(int argc, char **argv)
{
	long n;
	char *end_ptr;
	mpf_t float_result;
	mpz_t int_result;
	clock_t t1, t2, t3;
	char *float_str, *int_str;
	int float_strlen, int_strlen;

	if (argc != 2) {
		fprintf(stderr, "Usage: %s <n>\n", argv[0]);
		return EX_USAGE;
	}

	n = strtol(argv[1], &end_ptr, 10);
	if (*(argv[1]) == 0 || *end_ptr != 0) {
		fprintf(stderr, "Usage: %s <n>\n", argv[0]);
		fprintf(stderr, "Input was not a number\n");
		return EX_USAGE;
	}

	printf("Computing fib(%ld) in two different ways.\n", n);

	t1 = clock();
	mpz_init(int_result);
	mpz_fib_ui(int_result, n);
	t2 = clock();
	fib_float(&float_result, n);
	t3 = clock();

	printf("Integer computation took %lu ticks\nFloat computation took %lu ticks\n(at a rate of %d ticks per second)\n\n", t2-t1, t3-t2, CLOCKS_PER_SEC);

	/* Now convert the results of both methods to strings
	   and make sure they give the same answer. */
	
	float_strlen = gmp_asprintf(&float_str, "%.0Ff", float_result);
	mpf_clear(float_result);

	int_strlen = gmp_asprintf(&int_str, "%Zd", int_result);
	mpz_clear(int_result);

	if (float_strlen != int_strlen || strncmp(float_str, int_str, int_strlen) != 0) {
		fprintf(stderr, "%s: different methods gave different results! [%d; %d]\n\n",
			argv[0], float_strlen, int_strlen);
		return EX_SOFTWARE;
	}

	free(float_str);
	free(int_str);

	return 0;
}
